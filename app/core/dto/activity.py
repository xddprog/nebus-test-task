from pydantic import BaseModel


class ActivityModel(BaseModel):
    name: str
    childrens: list["ActivityModel"] = []
    
    class Config:
        from_attributes = True