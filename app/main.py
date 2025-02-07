from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers import all_routers
from app.infrastructure.database.adapters.pg_connection import DatabaseConnection


@asynccontextmanager
async def lifespan(app):
    app.state.db_connection = await DatabaseConnection()()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(all_routers)