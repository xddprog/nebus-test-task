from typing import Annotated
from fastapi import APIRouter, Depends

from app.api.v1.dependencies import get_activity_service, get_building_service, get_organization_service
from app.core.dto.organization import OrganizationFullModel, OrganizationModel
from app.core.services.activity_service import ActivityService
from app.core.services.building_service import BuildingService
from app.core.services.organization_service import OrganizationService


router = APIRouter()


@router.get("/all")
async def get_organizations(
    organization_service: Annotated[
        OrganizationService, Depends(get_organization_service)
    ],
    limit: int = 10,
    offset: int = 0,
    activity: int = None
) -> list[OrganizationModel]:
    return await organization_service.get_organizations(activity, limit, offset)


@router.get("/by_bbox")
async def get_organizations_within(
    xmin: float, 
    ymin: float, 
    xmax: float, 
    ymax: float,
    building_service: Annotated[BuildingService, Depends(get_building_service)]
) -> list[OrganizationModel]:
    return await building_service.get_organizations_within(xmin, ymin, xmax, ymax)


@router.get("/by_location")
async def get_organizations_nerby(
    lat: float,
    lon: float,
    radius: int,
    building_service: Annotated[BuildingService, Depends(get_building_service)],
) -> list[OrganizationModel]:
    return await building_service.get_organizations_nearby(lat, lon, radius)


@router.get("/by_name")
async def search_organizations(
    name: str,
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> OrganizationModel:
    return await organization_service.get_organization_by_name(name)


@router.get("/by_activity")
async def get_organizations_by_activity(
    activity: str,
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> list[OrganizationModel]:
    return await organization_service.get_organizations_by_activity(activity)


@router.get('/{organization_id}')
async def get_organization(
    organization_id: int,
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    activity_service: Annotated[ActivityService, Depends(get_activity_service)],
) -> OrganizationFullModel:
    activities = await activity_service.get_organization_activities(organization_id)
    return await organization_service.get_organization(organization_id, activities)
