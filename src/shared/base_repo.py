from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import TypeVar, Generic, Type, Optional, Any

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    async def create(self, data: BaseModel | dict) -> Optional[ModelType]:
        if isinstance(data, BaseModel):
            data = data.model_dump()
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def add_all(self, objects: list[Any]):
        self.session.add_all(objects)

    async def get(self, obj_id: int, user_id: Optional[int] = None) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == obj_id)

        if user_id is not None and hasattr(self.model, "user_id"):
            stmt = stmt.where(self.model.user_id == user_id, self.model.id == obj_id)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(self, user_id: Optional[int] = None) -> list[ModelType]:
        stmt = select(self.model)

        if user_id is not None and hasattr(self.model, "user_id"):
            stmt = stmt.where(self.model.user_id == user_id)
        print('user_id', stmt)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, obj_id: int, data: dict) -> Optional[ModelType]:
        obj = await self.get(obj_id)
        if not obj:
            return None
        if isinstance(data, BaseModel):
            data = data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(obj, key, value)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj_id: int, user_id) -> bool:
        obj = await self.get(obj_id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True
