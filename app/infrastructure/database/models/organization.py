from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.models.activity import Activity
from app.infrastructure.database.models.base import Base
from app.infrastructure.database.models.building import Building


class OrganizationPhone(Base):
    __tablename__ = "organizations_phones"

    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    phone_number: Mapped[str]

    organization: Mapped["Organization"] = relationship(
        "Organization", 
        back_populates="phone_numbers"
    )


class Organization(Base):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(unique=True)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"), nullable=False)

    building: Mapped["Building"] = relationship("Building", back_populates="organizations", lazy="selectin")
    activities: Mapped[list["Activity"]] = relationship(
        back_populates="organizations",
        secondary="organization_activities",
        lazy="selectin"
    )
    phone_numbers: Mapped[list["OrganizationPhone"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan", 
        lazy="selectin"
    )


class OrganizationActivity(Base):
    __tablename__ = "organization_activities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    activity_id: Mapped[int] = mapped_column(ForeignKey("activities.id"), nullable=False)
