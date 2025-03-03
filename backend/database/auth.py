from sqlmodel import Session, select

from backend.database.schema import DBRegistration, DBAccount
from backend.exceptions import EntityNotFound
from backend.utils import _hash_password  

def create_user(session: Session, username: str, password: str) -> DBAccount:
    """Register a new user in the system.
    
    Args:
        session (Session): The database session
        username (str): The username for the new user
        password (str): The user's password (to be hashed)
    
    Returns:
        DBUser: The newly created user
    """
    hashed_password = _hash_password(password)  
    new_user = DBAccount(username=username, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
