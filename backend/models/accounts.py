from typing import Optional
from pydantic import BaseModel

class Account(BaseModel):
    id: int | None 
    username: str 

class AccountCreate(BaseModel):
    """Request model for creating a new account."""

    username: str
    email: str
    password: str

class AccountUpdate(BaseModel):
    """Request model for updating an account."""

    username: Optional[str] = None
    email: Optional[str] = None