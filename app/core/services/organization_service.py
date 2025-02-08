from app.core.dto.activity import ActivityModel
from app.core.dto.building import BuildingModel
from app.core.dto.organization import OrganizationFullModel, OrganizationModel, OrganizationPhone
from app.core.repositories import OrganizationRepository
from app.infrastructure.errors.organization_errors import OrganizationNotFound


class OrganizationService:
    def __init__(self, repository: OrganizationRepository):
        self.repository = repository

    async def get_organization(self, organization_id: int, activities: list[ActivityModel]) -> OrganizationModel:
        organization = await self.repository.get_item(organization_id)
        if not organization:
            raise OrganizationNotFound
        return OrganizationFullModel(
            id=organization.id,
            name=organization.name,
            building=BuildingModel.model_validate(organization.building, from_attributes=True),
            activities=activities,
            phone_numbers=[
                OrganizationPhone.model_validate(phone, from_attributes=True) 
                for phone in organization.phone_numbers
            ]
        )

    async def get_organizations(self, activity: int, limit: int, offset: int) -> list[OrganizationModel]:
        organizations = await self.repository.get_with_activity(activity, limit, offset)
        return [
            OrganizationModel.model_validate(organization, from_attributes=True) 
            for organization in organizations
        ]
        
    async def get_building_organizations(self, building_id: int) -> list[OrganizationModel]:
        organizations = await self.repository.get_building_organizations(building_id)
        return [
            OrganizationModel.model_validate(organization, from_attributes=True) 
            for organization in organizations
        ]
    
    async def get_organization_by_name(self, name: str) -> OrganizationModel:
        organization = await self.repository.get_by_attributes(
            (self.repository.model.name, name),
            one_or_none=True
        )
        if not organization:
            raise OrganizationNotFound
        return OrganizationModel.model_validate(organization, from_attributes=True)
    
    async def get_organizations_by_activity(
        self, 
        activity: str, 
        limit: int, 
        offset: int
    ) -> list[OrganizationModel]:
        organizations = await self.repository.get_organizations_by_activity(activity, limit, offset)
        return [
            OrganizationModel.model_validate(organization, from_attributes=True) 
            for organization in organizations
        ]