from typing import Annotated, AsyncGenerator
from fastapi import Depends, Request

from sqlalchemy.ext.asyncio import AsyncSession

import app.core.repositories as repositories
import app.core.services as services


async def get_db_session(
    request: Request,
) -> AsyncGenerator[AsyncSession, None]:
    session = await request.app.state.db_connection.get_session()
    try:
        yield session
    finally:
        await session.close()


async def get_auth_service(session=Depends(get_db_session)):
    return services.AuthService(
        repository=repositories.UserRepository(session=session)
    )


async def check_token(
    request: Request, 
    auth_service: Annotated[services.AuthService, Depends(get_auth_service)]
):
    request = await request.json()
    return await auth_service.check_token(request.get("token"))
