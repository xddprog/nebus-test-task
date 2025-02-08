from typing import Annotated
from fastapi import APIRouter, Depends

from app.api.v1.dependencies import get_auth_service
from app.core.dto.auth import AuthUserModel
from app.core.services.auth_service import AuthService


router = APIRouter()


@router.post("/register")
async def register(
    form: AuthUserModel, 
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> str:
    return await auth_service.register_user(form)


@router.post("/login")
async def login(
    form: AuthUserModel, 
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> str:
    return await auth_service.login_user(form)