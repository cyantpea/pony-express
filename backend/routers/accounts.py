from fastapi import APIRouter
from sqlmodel import Session

from backend.dependencies import DBSession
from backend.models.accounts import Account
from backend.database import accounts as db_accounts

accounts_router = APIRouter(prefix="/accounts", tags=["Accounts"])

@accounts_router.get("/")
def accounts(session: DBSession):
    return db_accounts.get_all(session)

@accounts_router.get("/{account_id}", response_model=Account)
def get_account(session: DBSession, account_id: int):
    return db_accounts.get_by_id(session, account_id)

