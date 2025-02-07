from app.core.repositories import OrganizationRepository


class OrganizationService:
    def __init__(self, repository: OrganizationRepository):
        self.repository = repository
    