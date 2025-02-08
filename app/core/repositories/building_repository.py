from sqlalchemy import func, select
from app.core.repositories.base import SqlAlchemyRepository
from app.infrastructure.database.models.building import Building
from app.infrastructure.database.models.organization import Organization


class BuildingRepository(SqlAlchemyRepository):
    model = Building

    async def get_building_organizations(self, building_id: int) -> list[Organization]:
        building = await self.get_item(building_id)
        return building.organizations
    
    async def get_buildings_nearby(
        self, 
        lat: float, 
        lon: float, 
        radius: int, 
        limit: int, 
        offset: int
    ) -> list[Building]:
        distance_expr = (
            6371
            * func.acos(
                func.cos(func.radians(lat))
                * func.cos(func.radians(Building.latitude))
                * func.cos(func.radians(Building.longitude) - func.radians(lon))
                + func.sin(func.radians(lat))
                * func.sin(func.radians(Building.latitude))
            )
        )
        query = (
            select(Building, distance_expr.label("distance"))
            .where(distance_expr <= radius) 
            .order_by(distance_expr)
            .limit(limit)
            .offset(offset)
        )
        return (await self.session.execute(query)).scalars().all()
    
    async def get_organizations_within(
        self, 
        xmin: float, 
        ymin: float, 
        xmax: float, 
        ymax: float, 
        limit: int, 
        offset: int
    ) -> list[Organization]:
        query = (
            select(Organization)
            .join(Building)
            .where(
                Building.latitude >= ymin,
                Building.latitude <= ymax,
                Building.longitude >= xmin,
                Building.longitude <= xmax
            )
            .limit(limit)
            .offset(offset)
        )
        return (await self.session.execute(query)).scalars().all()