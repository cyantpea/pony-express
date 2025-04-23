import datetime
import jwt
import os

from dotenv import load_dotenv

from sqlmodel import Session, select

from backend.models.auth import AccessToken, Claims, Login, Registration
from backend.exceptions import DuplicateEntityValue, EntityNotFound, Forbidden, InvalidCredentials
from backend.utils import _hash_password, _verify_password  
from backend.database.schema import DBAccount
from backend.config import settings


load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_COOKIE_KEY = os.getenv("JWT_COOKIE_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ISSUER = os.getenv("JWT_ISSUER", "pony-express")
DURATION = os.getenv("JWT_DURATION", 3600)  # Default to 1 hour if not set


def create_user(session: Session, form: Registration) -> DBAccount:
    """Register a new user in the system.
    
    Args:
        session (Session): The database session
        form (Registration): The registration form data
    
    Returns:
        DBUser: The newly created user
    """

    existing_user = session.exec(select(DBAccount).where(DBAccount.username == form.username)).first()
    if existing_user:
        raise DuplicateEntityValue("username", form.username)
    
    existing_email = session.exec(select(DBAccount).where(DBAccount.email == form.email)).first()
    if existing_email:
        raise DuplicateEntityValue("email", form.email)

    hashed_password = _hash_password(form.password)  
    new_user = DBAccount(username=form.username, hashed_password=hashed_password, email=form.email)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

def generate_token(session: Session, form: Login) -> str:
    """Retrieve an access token for the user.
    
    Args:
        session (Session): The database session
        form (Login): The login form data
    
    Returns:
        str: The access token
    """

    account = session.exec(select(DBAccount).where(DBAccount.username == form.username)).first()
    
    account = validate_credentials(account, form.password)
    claims = generate_claims(account)

    return jwt.encode(
        claims.model_dump(),
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )
    
def generate_claims(account: DBAccount) -> Claims:
    iat = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    exp = iat + int(DURATION)
    return Claims(
        sub=str(account.id),
        iss=JWT_ISSUER,
        iat=iat,
        exp=exp,
    )

def validate_credentials(account: DBAccount | None, password: str) -> DBAccount:
    if account is None or not _verify_password(password, account.hashed_password):
        raise InvalidCredentials()
    
    return account

def get_access_token(session: Session, form: Login) -> AccessToken:
    """Retrieve an access token for the user.
    
    Args:
        session (Session): The database session
        form (Login): The login form data
    
    Returns:
        AccessToken: The access token
    """

    access_token = generate_token(session, form)
    return AccessToken(access_token=access_token, token_type="bearer")

def extract_account(session: Session, token: str) -> DBAccount:
    """Extract an account from a JWT.

    Args:
        session (Session): The database session
        token (str): The access token (JWT)

    Returns:
        DBAccount: The account tied to the token

    Raises:
        Forbidden: if the token is expired or invalid
        InvalidCredentials: if the account does not exist
    """


    if not token:
        raise Forbidden("authentication_required", "Not authenticated")
    try:
        claims = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise Forbidden("expired_access_token", "Authentication failed: expired access token")
    except jwt.InvalidTokenError:
        raise Forbidden("invalid_access_token", "Authentication failed: invalid access token")
    account_id = int(claims['sub'])  
    account = session.get(DBAccount, account_id)
    if account is None:
        raise InvalidCredentials()
    return account