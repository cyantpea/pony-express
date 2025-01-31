from sqlmodel import Session, select

from backend.database.schema import DBAccount
from backend.exceptions import EntityNotFound

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
