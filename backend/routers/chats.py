from fastapi import APIRouter

from backend.dependencies import engine, DBSession
from backend.models.chats import Chat, Message, ChatMembership
from backend.database import chats as db_chats

chats_router = APIRouter(prefix="/chats", tags=["Chats"])

@chats_router.get("/")
def chats(session: DBSession):
    return db_chats.get_all(session)

@chats_router.get("/{chat_id}")
def get_chat(session: DBSession, chat_id: int):
    return db_chats.get_by_id(session, chat_id)

@chats_router.get("/{chat_id}/accounts")
def get_chat_accounts(session: DBSession, chat_id: int):
    return db_chats.get_accounts_for_chat(session, chat_id)

@chats_router.get("/{chat_id}/messages") 
def get_chat_messages(session: DBSession, chat_id: int):
    return db_chats.get_messages_for_chat(session, chat_id)
