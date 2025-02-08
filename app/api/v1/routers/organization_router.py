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
    """
    Fetch a list of organizations, optionally filtered by activity ID.
    Args:
        limit (int, optional): The maximum number of organizations to return. Defaults to 10.
        offset (int, optional): The number of organizations to skip before starting to collect the result set. Defaults to 0.
        activity (int, optional): The activity ID to filter organizations by. If None, no filtering is applied. Defaults to None.
    Returns:
        list[OrganizationModel]: A list of organizations, optionally filtered by activity ID.
    """
    return await organization_service.get_organizations(activity, limit, offset)


@router.get("/by_bbox")
async def get_organizations_within(
    xmin: float, 
    ymin: float, 
    xmax: float, 
    ymax: float,
    building_service: Annotated[BuildingService, Depends(get_building_service)],
    limit: int = 10,
    offset: int = 0,
) -> list[OrganizationModel]:
    """
    Fetch a list of organizations within the specified bounding box.
    Args:
        xmin (float): The minimum x-coordinate (longitude) of the bounding box.
        ymin (float): The minimum y-coordinate (latitude) of the bounding box.
        xmax (float): The maximum x-coordinate (longitude) of the bounding box.
        ymax (float): The maximum y-coordinate (latitude) of the bounding box.
        limit (int, optional): The maximum number of organizations to return. Defaults to 10.
        offset (int, optional): The number of organizations to skip before starting to collect the result set. Defaults to 0.
    Returns:
        list[OrganizationModel]: A list of organizations within the specified bounding box.
    """
    return await building_service.get_organizations_within(xmin, ymin, xmax, ymax, limit, offset)


@router.get("/by_location")
async def get_organizations_nerby(
    lat: float,
    lon: float,
    radius: int,
    building_service: Annotated[BuildingService, Depends(get_building_service)],
    limit: int = 10,
    offset: int = 0,
) -> list[OrganizationModel]: 
    """
    Fetches a list of organizations nearby based on the given latitude, longitude, and radius.
    Args:
        lat (float): Latitude of the location to search nearby.
        lon (float): Longitude of the location to search nearby.
        radius (int): Radius (in kilometers) within which to search for organizations.
        limit (int, optional): Maximum number of organizations to return. Defaults to 10.
        offset (int, optional): Number of organizations to skip before starting to collect the result set. Defaults to 0.
    Returns:
        list[OrganizationModel]: A list of organizations within the specified radius.
    """
    return await building_service.get_organizations_nearby(lat, lon, radius, limit, offset)


@router.get(
    "/by_name", 
    responses={
        404: {
            "description": "Organization not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Organization not found"}
                }
            }
        }
    }
)
async def search_organizations(
    name: str,
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> OrganizationModel:
    return await organization_service.get_organization_by_name(name)


@router.get("/by_activity")
async def get_organizations_by_activity(
    activity: str,
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    limit: int = 10,
    offset: int = 0,
) -> list[OrganizationModel]:
    """
    Fetch a list of organizations based on their activity.
    Args:
        activity (str): The activity to filter organizations by.
        limit (int, optional): The maximum number of organizations to return. Defaults to 10.
        offset (int, optional): The number of organizations to skip before starting to collect the result set. Defaults to 0.
    Returns:
        list[OrganizationModel]: A list of organizations that match the specified activity.
    """
    return await organization_service.get_organizations_by_activity(activity, limit, offset)


@router.get(
    '/{organization_id}',
    responses={
        404: {
            "description": "Organization not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Organization not found"}
                }
            }
        }
    }
)
async def get_organization(
    organization_id: int,
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    activity_service: Annotated[ActivityService, Depends(get_activity_service)],
) -> OrganizationFullModel:
    """
    Retrieve an organization's full details including its activities.
    Args:
        organization_id (int): The unique identifier of the organization.
        organization_service (OrganizationService): The service to handle organization-related operations.
        activity_service (ActivityService): The service to handle activity-related operations.
    Returns:
        OrganizationFullModel: The full details of the organization including its activities.
    """
    activities = await activity_service.get_organization_activities(organization_id)
    return await organization_service.get_organization(organization_id, activities)
