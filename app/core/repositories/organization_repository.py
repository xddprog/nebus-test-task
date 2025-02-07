from app.core.repositories.base import SqlAlchemyRepository
from app.infrastructure.database.models.organization import Organization


class OrganizationRepository(SqlAlchemyRepository):
    model = Organization