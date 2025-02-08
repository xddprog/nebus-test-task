from contextlib import asynccontextmanager
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from app.core.repositories.base import SqlAlchemyRepository
from app.infrastructure.database.models.activity import Activity
from app.infrastructure.database.models.organization import Organization


class ActivityRepository(SqlAlchemyRepository):
    model = Activity

    async def get_organization_activities(self, organization_id: int) -> list[Activity]:
        query = (
            select(self.model)
            .where(
                self.model.organizations.any(Organization.id == organization_id)
            )
            # .options(selectinload(self.model.childrens))
        )
        return (await self.session.execute(query)).unique().scalars().all()