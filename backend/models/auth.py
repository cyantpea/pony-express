from pydantic import BaseModel

class Registration(BaseModel):
    username: str
    email: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class AccessToken(BaseModel):
    access_token: str
    token_type: str

class Claims(BaseModel):
    sub: str
    iss: str
    iat: int
    exp: int

class User(BaseModel):
    id: int
    username: str
    email: str
    