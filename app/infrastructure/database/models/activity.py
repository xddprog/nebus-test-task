from sqlalchemy.orm import Mapped, relationship

from app.infrastructure.database.models.base import Base


class Activity(Base):
    __tablename__ = "activities"
    name: Mapped[str]

    organization_activities = relationship(
        "OrganizationActivity", 
        back_populates="activity"
    )