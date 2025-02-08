from typing import Annotated
from fastapi import APIRouter, Depends

from app.api.v1.dependencies import get_building_service, get_organization_service
from app.core.dto.organization import OrganizationModel
from app.core.services.building_service import BuildingService
from app.core.services.organization_service import OrganizationService


router = APIRouter()


@router.get('/{building_id}/organizations')
async def get_building_organizations(
    building_id: int,
    organization_service: Annotated[
        OrganizationService, Depends(get_organization_service)
    ]
) -> list[OrganizationModel]:
    """
    Fetches the list of organizations associated with a specific building.
    Args:
        building_id (int): The ID of the building for which to fetch organizations.
    Returns:
        list[OrganizationModel]: A list of organizations associated with the specified building.
    """
    return await organization_service.get_building_organizations(building_id)