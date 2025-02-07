from app.core.repositories.base import SqlAlchemyRepository
from app.infrastructure.database.models.user import User


class UserRepository(SqlAlchemyRepository):
    model = User