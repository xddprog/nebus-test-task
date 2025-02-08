from app.core.dto.activity import ActivityModel
from app.core.repositories.activity_repository import ActivityRepository


class ActivityService:
    def __init__(self, repository: ActivityRepository):
        self.repository = repository

    async def get_organization_activities(self, organization_id: int) -> list[ActivityModel]:
        activities = await self.repository.get_organization_activities(organization_id)
        activities = [activity for activity in activities if activity.parent_id is None]
        return [
            ActivityModel.model_validate(activity, from_attributes=True)
            for activity in activities
        ]