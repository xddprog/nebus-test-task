from sqlalchemy import select
from app.core.repositories.base import SqlAlchemyRepository
from app.infrastructure.database.models.activity import Activity
from app.infrastructure.database.models.organization import Organization


class OrganizationRepository(SqlAlchemyRepository):
    model = Organization

    async def get_with_activity(self, activity: int, limit: int, offset: int) -> list[Organization]:
        query = (
            select(self.model)
            .where(self.model.activities.any(Activity.id == activity) if activity else True)
            .limit(limit)
            .offset(offset)
        )
        return (await self.session.execute(query)).scalars().all()

    async def get_building_organizations(self, building_id: int) -> list[Organization]:
        query = select(self.model).where(self.model.building_id == building_id)
        return (await self.session.execute(query)).scalars().all()

    async def get_organizations_by_activity(self, activity: str, limit: int, offset: int) -> list[Organization]:
        query = (
            select(self.model)
            .where(self.model.activities.any(Activity.name == activity))
            .limit(limit)
            .offset(offset)
        )
        return (await self.session.execute(query)).scalars().all()
    