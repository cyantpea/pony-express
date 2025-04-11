from sqlmodel import Session, select

from backend.database.schema import DBAccount
from backend.exceptions import DuplicateEntityValue, EntityNotFound
from backend.models.accounts import AccountUpdate

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

    existing_username = session.exec(select(DBAccount).where(DBAccount.username == updated_account.username)).first()
    if existing_username and existing_username.id != account_id:
        raise DuplicateEntityValue("username", updated_account.username)
    existing_email = session.exec(select(DBAccount).where(DBAccount.email == updated_account.email)).first()
    if existing_email and existing_email.id != account_id:
        raise DuplicateEntityValue("email", updated_account.email)
    
    if account.username != updated_account.username:
        setattr(account, "username", updated_account.username)
    if account.email != updated_account.email:  
        setattr(account, "email", updated_account.email)

    session.commit()
    session.refresh(account)

    return account
