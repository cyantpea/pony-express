from fastapi import APIRouter
from sqlmodel import Session

from backend.dependencies import DBSession
from backend.models.accounts import Account
from backend.database import accounts as db_accounts

accounts_router = APIRouter(prefix="/accounts", tags=["Accounts"])

@accounts_router.get("/")
def get_accounts(session: DBSession):
    accounts = db_accounts.get_all(session)

    response = {
        "metadata": {"count": len(accounts)},
        "accounts":  [{"id": account.id, "username": account.username} for account in accounts]
    }
    
    return response

@accounts_router.get("/{account_id}")
def get_account(session: DBSession, account_id: int):
    account = db_accounts.get_by_id(session, account_id)
    if account is not None:
        return {"id": account.id, "username": account.username}
    
    return EntityNotFound("account", account_id)
