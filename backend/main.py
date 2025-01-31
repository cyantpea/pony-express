"""PonyExpress backend API application.

Args:
    app (FastAPI): The FastAPI application
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel
from sqlmodel import Session

from backend.dependencies import create_db_tables
from backend.database.schema import DBAccount, DBChat, DBChatMembership, DBMessage


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield


app = FastAPI(
    title="Pony Express",
    summary="a messaging application",
    lifespan=lifespan,
)


# ========== router ==========
@app.get("/status", response_model=None, status_code=204)
def status():
    pass
