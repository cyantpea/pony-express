from fastapi import APIRouter

from backend.dependencies import  DBSession
from backend.database import chats as db_chats

chats_router = APIRouter(prefix="/chats", tags=["Chats"])

@chats_router.get("/")
def get_chats(session: DBSession):
    chats = db_chats.get_all(session)

    response = {
        "metadata": {"count": len(chats)},
        "chats": [{"id": chat.id, "name": chat.name, "owner_id": chat.owner_id} for chat in chats]
    }
    return response

@chats_router.get("/{chat_id}")
def get_chat(session: DBSession, chat_id: int):
    chat = db_chats.get_by_id(session, chat_id)
    return {"id": chat.id, "name": chat.name, "owner_id": chat.owner_id}

@chats_router.get("/{chat_id}/accounts")
def get_chat_accounts(session: DBSession, chat_id: int):
    accounts = db_chats.get_accounts_for_chat(session, chat_id)

    response = {
        "metadata": {"count": len(accounts)},
        "accounts":  [{"id": account.id, "username": account.username} for account in accounts]
    }
    
    return response

@chats_router.get("/{chat_id}/messages") 
def get_chat_messages(session: DBSession, chat_id: int):
    messages = db_chats.get_messages_for_chat(session, chat_id)

    response = {
        "metadata": {"count": len(messages)},
        "messages": [{"id": message.id, "text": message.text, "account_id": message.account_id, "chat_id": message.chat_id, "created_at": message.created_at} for message in messages]
    }

    return response
