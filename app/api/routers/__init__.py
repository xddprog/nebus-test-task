from fastapi import APIRouter, Depends

from app.api.dependencies import check_token
from app.api.routers.auth_router import router as auth_router


all_routers = APIRouter(prefix="/api/v1")
PROTECTED = Depends(check_token)


all_routers.include_router(auth_router, tags=["AUTH"], prefix="/auth")