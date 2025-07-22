from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from src.shared.db import Trigger


class TriggerRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: dict) -> Trigger:
        obj = Trigger(**data)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get(self, obj_id: int) -> Optional[Trigger]:
        result = await self.session.execute(select(Trigger).where(Trigger.id == obj_id))
        return result.scalar_one_or_none()

    async def list(self) -> list[Trigger]:
        result = await self.session.execute(select(Trigger))
        return result.scalars().all()

    async def update(self, obj_id: int, data: dict) -> Optional[Trigger]:
        obj = await self.get(obj_id)
        if not obj:
            return None
        for key, value in data.items():
            setattr(obj, key, value)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj_id: int) -> bool:
        obj = await self.get(obj_id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True
