from app.core.repositories.building_repository import BuildingRepository


class BuildingService:
    def __init__(self, repository: BuildingRepository):
        self.repository = repository
    