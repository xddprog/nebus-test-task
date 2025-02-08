from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.models.base import Base


class Building(Base):
    __tablename__ = "buildings"

    address: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]
    
    organizations = relationship(
        "Organization", 
        back_populates="building", 
        lazy="selectin",
        cascade="all, delete"
    )
