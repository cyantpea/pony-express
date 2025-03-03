from fastapi import Response
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class NotFound(BaseModel):
    error: str
    message: str

class EntityNotFound(HTTPException):
    def __init__(self, entity_name: str, entity_id: int):
        self.content = NotFound(
            error="entity_not_found",
            message=f"Unable to find {entity_name} with id={entity_id}",
        )
        self.status_code = 404
    
    def response(self) -> Response:
        return JSONResponse(
            status_code=self.status_code,
            content=self.content.model_dump()
        )

class Forbidden(HTTPException):
    def __init__(self, error: str, message: str):
        self.error = error
        self.message = message
        self.status_code = 403
    
    def response(self) -> Response:
        return JSONResponse(
            status_code=self.status_code,
            error=self.error,
            message=self.message
        )


def authentication_required():
    return Forbidden("authentication_required", "Not authenticated")

def expired_access_token():
    return Forbidden("expired_access_token", "Authentication failed: expired access token")

def invalid_access_token():
    return Forbidden("invalid_access_token", "Authentication failed: invalid access token")