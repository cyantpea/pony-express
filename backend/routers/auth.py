from fastapi import APIRouter, Depends, Form, Response
from typing import Annotated
from sqlmodel import Session

from backend.database.schema import DBAccount
from backend.dependencies import  DBSession, get_current_account
from backend.models.auth import Login, Registration, User
from backend.database import auth as db_auth


auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/registration", status_code=201)
def register_new_user(session: DBSession, form: Annotated[Registration, Form()]) -> User:
    registered_user = db_auth.create_user(session, form)

    return {
        "id": registered_user.id,
        "username": registered_user.username,
        "email": registered_user.email
    }

@auth_router.post("/token", status_code=200)
def get_token(session: DBSession, form: Annotated[Login, Form()]):
    access_token = db_auth.get_access_token(session, form)

    return {
        "access_token": access_token.access_token,
        "token_type": access_token.token_type
    }

@auth_router.post("/web/login", status_code=204)
def login(session: DBSession, form: Annotated[Login, Form()], response: Response):
    access_token = db_auth.get_access_token(session, form)

    response.set_cookie(
        key=db_auth.JWT_COOKIE_KEY,
        value=access_token.access_token,
        httponly=True,
        samesite="None",
        secure=True,
        max_age=3600
    )
    
   
    

@auth_router.post(
        "/web/logout", 
        status_code=204,
        dependencies=[Depends(get_current_account)])
def logout(response: Response):
    response.delete_cookie(key=db_auth.JWT_COOKIE_KEY)
    



