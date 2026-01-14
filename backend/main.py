"""PonyExpress backend API application.

Args:
    app (FastAPI): The FastAPI application
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from backend.dependencies import create_db_tables
from backend.routers.accounts import accounts_router
from backend.routers.chats import chats_router
from backend.routers.auth import auth_router
from backend.exceptions import CustomHTTPException


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield


app = FastAPI(
    title="Pony Express",
    summary="a messaging application",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

for router in [accounts_router, chats_router, auth_router]:
    app.include_router(router)

# ========== router ==========
@app.get("/status", response_model=None, status_code=204)
def status():
    pass

# ========== exception handlers ==========
@app.exception_handler(CustomHTTPException)
def handle_exceptions(request: Request, exception: CustomHTTPException):
    return exception.response()
