from fastapi import Response
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class Error(BaseModel):
    error: str
    message: str

class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, error: str, message: str):
        super().__init__(status_code=status_code)
        self.content = Error(
            error=error,
            message=message
        )

    def response(self) -> Response:
        return JSONResponse(
            status_code=self.status_code,
            content=self.content.model_dump()
        )
    
class EntityNotFound(CustomHTTPException):
    def __init__(self, entity_name: str, entity_id: int):
        self.content = Error(
            error="entity_not_found",
            message=f"Unable to find {entity_name} with id={entity_id}",
        )
        self.status_code = 404
    
    def response(self) -> Response:
        return JSONResponse(
            status_code=self.status_code,
            content=self.content.model_dump()
        )

class DuplicateEntity(CustomHTTPException):
    def __init__(self, entity_name: str):
        self.content = Error(
            error="duplicate_entity_value",
            message=f"Duplicate value: chat with name={entity_name} already exists"
        )
        self.status_code = 422
    
    def response(self) -> Response:
        return JSONResponse(
            status_code=self.status_code,
            content=self.content.model_dump()
        )
    
class Forbidden(CustomHTTPException):
    def __init__(self, error: str, message: str):
        self.content = Error(
            error = error,
            message = message
        )
        self.status_code = 403
    
    def response(self) -> Response:
        return JSONResponse(
            status_code=self.status_code,
            content=self.content.model_dump()
        )

class ChatMembershipRequired(CustomHTTPException):
    def __init__(self, account_id: int, chat_id: int):
        self.content = Error(
            error="chat_membership_required",
            message=f"Account with id={account_id} must be a member of chat with id={chat_id}"
        )
        self.status_code = 422
    
    def response(self) -> Response:
        return JSONResponse(
            status_code=self.status_code,
            content=self.content.model_dump()
        )
    
class ChatOwnerRemoval(CustomHTTPException):
    def __init__(self):
        self.content = Error(
            error="chat_owner_removal",
            message="Unable to remove the owner of a chat"
        )
        self.status_code = 422
    
    def response(self) -> Response:
        return JSONResponse(
            status_code=self.status_code,
            content=self.content.model_dump()
        )
    
class DuplicateEntityValue(CustomHTTPException):
    def __init__(self, entity_name: str, entity_value: str):
        self.content = Error(
            error="duplicate_entity_value",
            message=f"Duplicate value: account with {entity_name}={entity_value} already exists"
        )
        self.status_code = 422
    
    def response(self) -> Response:
        return JSONResponse(
            status_code=self.status_code,
            content=self.content.model_dump()
        )
    
class InvalidCredentials(CustomHTTPException):
    def __init__(self):
        self.content = Error(
            error="invalid_credentials",
            message="Authentication failed: invalid username or password"
        )
        self.status_code = 401
    
    def response(self) -> Response:
        return JSONResponse(
            status_code=self.status_code,
            content=self.content.model_dump()
        )

def authentication_required():
    return Forbidden("authentication_required", "Not authenticated")

def expired_access_token():
    return Forbidden("expired_access_token", "Authentication failed: expired access token")

def invalid_access_token():
    return Forbidden("invalid_access_token", "Authentication failed: invalid access token")