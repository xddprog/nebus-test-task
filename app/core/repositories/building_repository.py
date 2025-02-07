from app.core.repositories.base import SqlAlchemyRepository
from app.infrastructure.database.models.building import Building


class BuildingRepository(SqlAlchemyRepository):
    model = Building