from sqlmodel import Session, select

from backend.database.schema import DBAccount, DBChat
from backend.exceptions import ChatOwnerRemoval, DuplicateEntityValue, EntityNotFound, InvalidCredentials
from backend.models.accounts import AccountUpdate
from backend.utils import _hash_password, _verify_password

def get_all(session: Session) -> list[DBAccount]:
    """Retrieve all accounts from database.
    
    Args:
        session (Session): The database session
    
    Returns:
        list[DBAccount]: The list of accounts
    """

    stmt = select(DBAccount)
    results = session.exec(stmt)
    return list(results)

def get_by_id(session: Session, account_id: int) -> DBAccount:
    """Retrieve specific account from database.
    
    Args:
        session (Session): The database session
        account_id (int): The id of the account to retrieve
    
    Returns:
        DBAccount: The account

    Raises:
        EntityNotFound: If no account with given id exists
    """
    
    account = session.get(DBAccount, account_id)
    if account is None:
        raise EntityNotFound("account", account_id)
    return account

def update_account(session: Session, account_id: int, updated_account: AccountUpdate) -> DBAccount:
    """Update an account in the database.
    
    Args:
        session (Session): The database session
        account_id (int): The id of the account to update
        updated_account (AccountUpdate): The updated account data
    
    Returns:
        DBAccount: The updated account
    """
    
    account = get_by_id(session, account_id)

    if updated_account.username is None and updated_account.email is None:
        return account
    
    if updated_account.username is not None:
        existing_username = session.exec(select(DBAccount).where(DBAccount.username == updated_account.username)).first()
        if existing_username and existing_username.id != account_id:
            raise DuplicateEntityValue("username", updated_account.username)
        
        if account.username != updated_account.username:
            setattr(account, "username", updated_account.username)
    if updated_account.email is not None:
        existing_email = session.exec(select(DBAccount).where(DBAccount.email == updated_account.email)).first()
        if existing_email and existing_email.id != account_id:
            raise DuplicateEntityValue("email", updated_account.email)
        
        if account.email != updated_account.email:  
            setattr(account, "email", updated_account.email)

    session.commit()
    session.refresh(account)

    return account

def update_password(session: Session, account: DBAccount, old_password: str, new_password: str):
    """Update the password of an account.
    
    Args:
        account (DBAccount): The account to update
        old_password (str): The old password
        new_password (str): The new password
    
    Raises:
        InvalidCredentials: If the old password is incorrect
    """
    
    if not _verify_password(old_password, account.hashed_password):
        raise InvalidCredentials()
    
    account.hashed_password = _hash_password(new_password)
    session.commit()
    session.refresh(account)

def delete_account(session: Session, account_id: int):
    """Delete an account from the database.
    
    Args:
        session (Session): The database session
        account_id (int): The id of the account to delete
    """
    
    account = get_by_id(session, account_id)
    owned_chats = session.exec(select(DBChat).where(DBChat.owner_id == account.id)).all()
    if len(owned_chats) > 0:
        raise ChatOwnerRemoval()

    session.delete(account)
    session.commit()
