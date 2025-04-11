from fastapi import APIRouter, Depends

from backend.dependencies import CurrentAccount, DBSession, get_current_account
from backend.exceptions import EntityNotFound
from backend.database import accounts as db_accounts
from backend.models.accounts import AccountUpdate

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
        "username": updated_account.username,
        "email": updated_account.email
    }   
    

@accounts_router.put("/me/password")
def reset_password():
    return

@accounts_router.delete("/me")
def delete_me():
    return