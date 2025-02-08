from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.testing.util import lazy_gc

from app.infrastructure.database.models.base import Base


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    parent_id: Mapped[int] = mapped_column(ForeignKey("activities.id"), nullable=True)

    parent: Mapped["Activity"] = relationship(remote_side=[id], lazy="selectin")
    childrens: Mapped[list["Activity"]] = relationship(
        back_populates="parent",
        lazy="joined",
        cascade="all, delete-orphan",
        join_depth=100
    )
    organizations = relationship(
        "Organization", 
        back_populates="activities", 
        secondary="organization_activities",
        lazy="selectin"
    )