from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.routers import all_routers
from app.infrastructure.database.adapters.pg_connection import DatabaseConnection
from app.utils.test_db import test_db


@asynccontextmanager
async def lifespan(app):
    app.state.db_connection = await DatabaseConnection()()
    await test_db(await app.state.db_connection.get_session())
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(all_routers)