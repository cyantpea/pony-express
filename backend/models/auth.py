from pydantic import BaseModel

class Registration(BaseModel):
    id: int
    account_id: int