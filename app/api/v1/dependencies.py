from typing import Annotated, AsyncGenerator
from fastapi import Depends, Request

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

import app.core.repositories as repositories
import app.core.services as services


token = HTTPBearer(auto_error=False)


async def get_db_session(
    request: Request,
) -> AsyncGenerator[AsyncSession, None]:
    session = await request.app.state.db_connection.get_session()
    try:
        yield session
    finally:
        await session.close()


async def get_auth_service(session=Depends(get_db_session)) -> services.AuthService:
    return services.AuthService(
        repository=repositories.UserRepository(session=session)
    )


async def check_token(
    auth_service: Annotated[services.AuthService, Depends(get_auth_service)],
    token: HTTPAuthorizationCredentials = Depends(token)
) -> None:
    return await auth_service.check_token(token)


async def get_building_service(session=Depends(get_db_session)) -> services.BuildingService:
    return services.BuildingService(
        repository=repositories.BuildingRepository(session=session)
    )


async def get_organization_service(session=Depends(get_db_session)) -> services.OrganizationService:
    return services.OrganizationService(
        repository=repositories.OrganizationRepository(session=session)
    )


async def get_activity_service(session=Depends(get_db_session)) -> services.ActivityService:
    return services.ActivityService(
        repository=repositories.ActivityRepository(session=session)
    )