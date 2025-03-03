"""PonyExpress backend API application.

Args:
    app (FastAPI): The FastAPI application
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from backend.dependencies import create_db_tables
from backend.routers.accounts import accounts_router
from backend.routers.chats import chats_router
from backend.exceptions import EntityNotFound


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield


app = FastAPI(
    title="Pony Express",
    summary="a messaging application",
    lifespan=lifespan,
)

for router in [accounts_router, chats_router]:
    app.include_router(router)

# ========== router ==========
@app.get("/status", response_model=None, status_code=204)
def status():
    pass

@app.exception_handler(EntityNotFound)
def handle_not_found(request: Request, exception: EntityNotFound):
    return exception.response()
