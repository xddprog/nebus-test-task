from fastapi import APIRouter, Depends

from app.api.v1.dependencies import check_token
from app.api.v1.routers.auth_router import router as auth_router
from app.api.v1.routers.building_router import router as building_router
from app.api.v1.routers.organization_router import router as organization_router


PROTECTED = Depends(check_token)
all_routers = APIRouter(prefix="/api/v1")


all_routers.include_router(auth_router, tags=["AUTH"], prefix="/auth")
all_routers.include_router(
    building_router, 
    tags=["BUILDING"], 
    prefix="/building", 
    # dependencies=[PROTECTED]
)
all_routers.include_router(
    organization_router, 
    tags=["ORGANIZATION"], 
    prefix="/organization", 
    # dependencies=[PROTECTED]
)
