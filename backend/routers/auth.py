from fastapi import APIRouter, Form
from typing import Annotated
from sqlmodel import Session

from backend.dependencies import  DBSession
from backend.models.auth import Registration
from backend.models.accounts import Account
from backend.database import auth


auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/registration", status_code=201)
def register_new_user(session: DBSession, form: Annotated[Registration, Form()]) -> Account:
    return create_user(session, form)
