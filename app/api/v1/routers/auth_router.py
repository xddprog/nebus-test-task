from typing import Annotated
from fastapi import APIRouter, Depends

from app.api.v1.dependencies import get_auth_service
from app.core.dto.auth import AuthUserModel
from app.core.dto.user import UserModel
from app.core.services.auth_service import AuthService


router = APIRouter()


@router.post(
    "/register",
    responses={
        400: {
            "description": "Organization not found",
            "content": {
                "application/json": {
                    "example": {"detail": "User already registered"}
                }
            }
        }
    }
)
async def register(
    form: AuthUserModel, 
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> UserModel:
    """
    Registers a new user.
    Args:
        form (AuthUserModel): The user registration form containing user details.
    Returns:
        UserModel: The registered user model.
    """
    return await auth_service.register_user(form)


@router.post(
    "/login",
    responses={
        404: {
            "content": {
                "application/json": {
                    "example": {"detail": "User not found"}
                }
            }
        }
    }
)
async def login(
    form: AuthUserModel, 
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> UserModel:
    """
    Logs in a user with the provided authentication form.

    Args:
        form (AuthUserModel): The user registration form containing user details.
    Returns:
        UserModel: The authenticated user model.
    """
    return await auth_service.login_user(form)