from abc import ABC, abstractmethod
from typing import Any, Type

from pydantic import UUID4
from sqlalchemy import Result, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import MappedColumn

from app.infrastructure.database.models.activity import Activity
from app.infrastructure.database.models.building import Building
from app.infrastructure.database.models.organization import Organization
from app.infrastructure.database.models.user import User



ModelType = Type[User | Organization | Activity | Building]


class BaseRepository(ABC):
    @abstractmethod
    async def get_item(self, item_id: int) -> ModelType | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_items(self) -> list[ModelType] | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_attributes(
        self, attribute: Any, value: int
    ) -> list[ModelType] | None:
        raise NotImplementedError

    @abstractmethod
    async def add_item(self, **kwargs: int) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    async def delete_item(self, item: ModelType) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_item(
        self, item_id: int | str, **update_values: str | int | UUID4
    ) -> ModelType:
        raise NotImplementedError


class SqlAlchemyRepository(BaseRepository):
    model: ModelType
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_item(self, item_id: int | UUID4 | str) -> ModelType:
        item = await self.session.get(self.model, item_id)
        return item

    async def get_all_items(self) -> list[ModelType]:
        query = select(self.model)
        items: Result = await self.session.execute(query)
        return items.scalars().all()

    async def get_by_attributes(
        self, 
        *attributes: tuple[tuple[MappedColumn[Any], str]],
        one_or_none: bool = False
    ) -> list[ModelType] | None:
        query = select(self.model)
        for attribute, value in attributes:
            query = query.where(attribute == value)
        result: Result = await self.session.execute(query)
        return result.scalars().all() if not one_or_none else result.scalar_one_or_none()

    async def add_item(self, **kwargs: int | str | UUID4) -> ModelType:
        item = self.model(**kwargs)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def delete_item(self, item: ModelType) -> None:
        await self.session.delete(item)
        await self.session.commit()

    async def update_item(
        self, 
        item_fk: MappedColumn[Any], 
        item_id: int | str, 
        **update_values
    ) -> ModelType:
        query = (
            update(self.model)
            .where(item_fk == item_id)
            .values(update_values)
            .returning(self.model)
        )
        item: Result = await self.session.execute(query)
        item = item.scalar_one_or_none()
        await self.session.commit()
        await self.session.refresh(item)
        return item