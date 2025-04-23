from typing import Annotated
from fastapi import APIRouter, Depends, Form

from backend.dependencies import CurrentAccount, DBSession, get_current_account
from backend.exceptions import EntityNotFound
from backend.database import accounts as db_accounts
from backend.models.accounts import AccountUpdate, UpdatePassword

accounts_router = APIRouter(prefix="/accounts", tags=["Accounts"])

@accounts_router.get("/")
def get_accounts(session: DBSession):
    accounts = db_accounts.get_all(session)

    response = {
        "metadata": {"count": len(accounts)},
        "accounts":  [{"id": account.id, "username": account.username} for account in accounts]
    }
    
    return response

@accounts_router.get("/me", status_code=200)
def get_self(account: CurrentAccount):
    
    return {
        "id": account.id,
        "username": account.username,
        "email": account.email
    }
    

@accounts_router.put("/me", status_code=200)
def update_self(session: DBSession, updated_account: AccountUpdate, account: CurrentAccount):
    db_accounts.update_account(session, account.id, updated_account)
    return {
        "id": account.id,
        "username": account.username,
        "email": account.email
    }   
    

@accounts_router.put("/me/password", status_code=204)
def new_password(session: DBSession, account: CurrentAccount, form: Annotated[UpdatePassword, Form()]):
    db_accounts.update_password(session, account, form.old_password, form.new_password)
    

@accounts_router.delete("/me", status_code=204)
def delete_me(account: CurrentAccount, session: DBSession):
    db_accounts.delete_account(session, account.id)

@accounts_router.get("/{account_id}")
def get_account(session: DBSession, account_id: int):
    account = db_accounts.get_by_id(session, account_id)
    if account is not None:
        return {"id": account.id, "username": account.username}
    
    return EntityNotFound("account", account_id)

