from app.core.dto.organization import OrganizationModel
from app.core.repositories.building_repository import BuildingRepository


class BuildingService:
    def __init__(self, repository: BuildingRepository):
        self.repository = repository

        
    async def get_organizations_within(
        self, 
        xmin: float, 
        ymin: float, 
        xmax: float,
        ymax: float,
        limit: int,
        offset: int
    ) -> list[OrganizationModel]:
        organizations = await self.repository.get_organizations_within(
            xmin, ymin, xmax, ymax, limit, offset
        )
        return [
            OrganizationModel.model_validate(organization, from_attributes=True) 
            for organization in organizations
        ]
    
    async def get_organizations_nearby(
        self, 
        lat: float, 
        lon: float, 
        radius: int,
        limit: int,
        offset: int
    ) -> list[OrganizationModel]:
        buildings = await self.repository.get_buildings_nearby(
            lat, lon, radius, limit, offset
        )
        return [
            OrganizationModel.model_validate(organization, from_attributes=True) 
            for building in buildings
            for organization in building.organizations
        ]