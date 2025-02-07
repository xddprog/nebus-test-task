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

    building: Mapped["Building"] = relationship("Building", back_populates="organizations")
    activities: Mapped[list["Activity"]] = relationship(
        "Activity", 
        secondary="organization_activities", 
        back_populates="organizations"
    )
    phone_numbers: Mapped[list["OrganizationPhone"]] = relationship(
        back_populates="organization"
    )


class OrganizationActivity(Base):
    __tablename__ = "organization_activities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    activity_id: Mapped[int] = mapped_column(ForeignKey("activities.id"), nullable=False)

    parent_id: Mapped[int] = mapped_column(ForeignKey("organization_activities.id"), nullable=True)
    parent: Mapped["OrganizationActivity"] = relationship(
        "OrganizationActivity", 
        back_populates="childrens", 
        remote_side=[id], 
        lazy="selectin"
    )
    childrens: Mapped[list["OrganizationActivity"]] = relationship(
        "OrganizationActivity", 
        back_populates="parent", 
        lazy="selectin", 
        cascade="all, delete-orphan"
    )
    organization: Mapped["Organization"] = relationship(
        "Organization", 
        back_populates="organization_activities"
    )
    activity: Mapped["Activity"] = relationship(
        "Activity", 
        back_populates="organization_activities"
    )

