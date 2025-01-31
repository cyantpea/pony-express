from pydantic import BaseModel

class Account(BaseModel):
    id: int | None 
    username: str 