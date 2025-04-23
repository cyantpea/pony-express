"""Dependencies for the backend API.

Args:
    engine (sqlalchemy.engine.Engine): The database engine
"""
from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyCookie, HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import SQLModel, create_engine, Session, text

from backend.database.schema import *
from backend.database import auth as db_auth
from backend.exceptions import Forbidden, InvalidCredentials
from backend.config import settings

_db_filename = "backend/database/development.db"
_db_url = f"sqlite:///{_db_filename}"
_connect_args = {"check_same_thread": False}
engine = create_engine(_db_url, echo=True, connect_args=_connect_args)
cookie_scheme = APIKeyCookie(name=settings.jwt_cookie_key, auto_error=False)
bearer_scheme = HTTPBearer(auto_error=False)


def create_db_tables():
    SQLModel.metadata.create_all(engine)
    with engine.connect() as connection:
        connection.execute(text("PRAGMA foreign_keys=ON"))


def get_session():
    with Session(engine) as session:
        yield session

def get_token(
    cookie_token: str | None = Depends(cookie_scheme),
    bearer: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    """Token extraction dependency.

    Depends on the cookie scheme and the bearer scheme.
    """

    if cookie_token is not None:
        return cookie_token
    if bearer is not None:
        return bearer.credentials
    raise Forbidden("authentication_required", "Not authenticated")

def get_current_account(
    session: Session = Depends(get_session),
    token: str = Depends(get_token),
) -> DBAccount:
    """Current account dependency.

    Depends on the session and the token.
    """

    return db_auth.extract_account(session, token)



CurrentAccount = Annotated[DBAccount, Depends(get_current_account)]
DBSession = Annotated[Session, Depends(get_session)]