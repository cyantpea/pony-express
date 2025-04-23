from fastapi import APIRouter, Response

from backend.dependencies import  CurrentAccount, DBSession
from backend.database import chats as db_chats
from backend.models import chats as model_chats

chats_router = APIRouter(prefix="/chats", tags=["Chats"])

@chats_router.get("/")
def get_chats(session: DBSession):
    chats = db_chats.get_all(session)

    response = {
        "metadata": {"count": len(chats)},
        "chats": [{"id": chat.id, "name": chat.name, "owner_id": chat.owner_id} for chat in chats]
    }
    return response

@chats_router.post("/", status_code=201)
def put_chats(session: DBSession, chat: model_chats.ChatCreate, account: CurrentAccount):
    new_chat = db_chats.create_chat(session, chat, account.id)

    return {
        "id": new_chat.id,
        "name": new_chat.name,
        "owner_id": new_chat.owner_id
    }

@chats_router.get("/{chat_id}")
def get_chat(session: DBSession, chat_id: int):
    chat = db_chats.get_by_id(session, chat_id)
    return {"id": chat.id, "name": chat.name, "owner_id": chat.owner_id}

@chats_router.put("/{chat_id}", status_code=200)
def update_chat(session: DBSession, chat_id: int, chat: model_chats.ChatUpdate):
    updated_chat = db_chats.update_chat(session, chat_id, chat)

    return {
        "id": updated_chat.id,
        "name": updated_chat.name,
        "owner_id": updated_chat.owner_id
    }

@chats_router.delete("/{chat_id}", status_code=204)
def delete_chat(session: DBSession, chat_id: int):
    db_chats.delete_chat(session, chat_id)

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

@chats_router.post("/{chat_id}/messages", status_code=201)
def post_chat_messages(session: DBSession, chat_id: int, message: model_chats.MessageCreate, account: CurrentAccount):
    new_message = db_chats.add_message(session, chat_id, message, account.id)

    return {
        "id": new_message.id,
        "text": new_message.text,
        "chat_id": new_message.chat_id,
        "created_at": new_message.created_at,
        "account_id": account.id
    }

@chats_router.put("/{chat_id}/messages/{message_id}", status_code=200)
def add_message(session: DBSession, chat_id: int, message_id: int, message: model_chats.MessageUpdate):
    updated_message = db_chats.update_message(session, chat_id, message_id, message)

    return {
        "id": updated_message.id,
        "text": updated_message.text,
        "chat_id": updated_message.chat_id,
        "created_at": updated_message.created_at,
        "account_id": updated_message.id
    }

@chats_router.delete("/{chat_id}/messages/{message_id}", status_code=204)
def delete_message(session: DBSession, chat_id: int, message_id: int):
    db_chats.delete_message(session=session, chat_id=chat_id, message_id=message_id)

@chats_router.post("/{chat_id}/accounts", status_code=200)
def add_account_to_chat(response: Response, session: DBSession, chat_id: int, chat_membership: model_chats.ChatMembershipCreate):
    existing_membership = db_chats.get_membership_by_ids(session, chat_id, chat_membership.account_id)
    if existing_membership:
        return {
            "chat_id": existing_membership.chat_id,
            "account_id": existing_membership.account_id
        }
    
    new_membership = db_chats.add_membership(session=session, chat_id=chat_id, chat_membership=chat_membership)
    response.status_code = 201

    return {
        "chat_id": new_membership.chat_id,
        "account_id": new_membership.account_id
    }

@chats_router.delete("/{chat_id}/accounts/{account_id}", status_code=204)
def remove_account_from_chat(session: DBSession, chat_id: int, account_id: int):
    db_chats.delete_membership(session, chat_id, account_id)