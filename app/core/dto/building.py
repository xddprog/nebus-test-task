from pydantic import BaseModel


class BuildingModel(BaseModel):
    id: int
    longitude: float
    latitude: float