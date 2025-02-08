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
    return await organization_service.get_building_organizations(building_id)