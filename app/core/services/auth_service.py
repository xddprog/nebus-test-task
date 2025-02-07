from uuid import uuid4

from app.core.dto.auth import AuthUserModel
from app.core.repositories.user_repository import UserRepository
from app.infrastructure.database.models.user import User
from app.infrastructure.errors.auth_errors import AccessDenied
from app.infrastructure.errors.user_errors import UserAlreadyRegistered, UserNotFound


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def _get_by_email(self, email: str) -> User:
        return await self.repository.get_by_attributes(
            (self.repository.model.email, email),
            one_or_none=True
        )
    
    async def _get_by_token(self, token: str) -> User:
        return await self.repository.get_by_attributes(
            (self.repository.model.token, token),
            one_or_none=True
        )

    async def register_user(self, form: AuthUserModel) -> str:
        user_exist = await self._get_by_email(form.email)
        if user_exist:
            raise UserAlreadyRegistered
        
        token = str(uuid4())
        await self.repository.add_item(
            email=form.email,
            password=form.password,
            token=token
        )
        return token

    async def login_user(self, form: AuthUserModel) -> str:
        user_exist = await self._get_by_email(form.email)
        if not user_exist:
            raise UserNotFound
        return user_exist.token
    
    async def check_token(self, token: str) -> None:
        user = await self._get_by_token(token)
        if not user:
            raise AccessDenied