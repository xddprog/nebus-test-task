from app.core.repositories.base import SqlAlchemyRepository
from app.infrastructure.database.models.activity import Activity


class ActivityRepository(SqlAlchemyRepository):
    model = Activity