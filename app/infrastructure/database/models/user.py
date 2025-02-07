from sqlalchemy.orm import Mapped
from app.infrastructure.database.models.base import Base


class User(Base):
    __tablename__ = "users"

    email: Mapped[str]
    password: Mapped[str]
    token: Mapped[str]