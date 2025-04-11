from datetime import datetime
from typing import Optional
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

class ChatCreate(BaseModel):
    """Request model for creating a new chat."""

    name: str
    owner_id: int

class ChatUpdate(BaseModel):
    """Request model for updating a chat."""

    name: Optional[str] = None
    owner_id: Optional[int] = None

class ChatMembershipCreate(BaseModel):
    """Request model for creating a new chat membership."""

    account_id: int

class MessageCreate(BaseModel):
    """Request model for creating a new message."""

    text: str
    account_id: int

class MessageUpdate(BaseModel):
    """Request model for updating a message."""
    text: str