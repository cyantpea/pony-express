from datetime import datetime
from pydantic import BaseModel

class Chat(BaseModel):
    id: int | None
    name: str
    owner_id: int

class Message(BaseModel):
    id: int | None 
    text: str
    account_id: int 
    chat_id: int 
    created_at: datetime | None

class ChatMembership(BaseModel):
    account_id: int
    chat_id: int