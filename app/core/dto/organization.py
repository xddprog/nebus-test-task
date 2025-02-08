from pydantic import BaseModel

from app.core.dto.activity import ActivityModel
from app.core.dto.building import BuildingModel


class OrganizationPhone(BaseModel):
    phone_number: str


class OrganizationModel(BaseModel):
    id: int
    name: str
    

class OrganizationFullModel(OrganizationModel):
    activities: list[ActivityModel]
    phone_numbers: list[OrganizationPhone]
    building: BuildingModel