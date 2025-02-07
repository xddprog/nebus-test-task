from app.core.repositories.activity_repository import ActivityRepository


class ActivityService:
    def __init__(self, repository: ActivityRepository):
        self.repository = repository
