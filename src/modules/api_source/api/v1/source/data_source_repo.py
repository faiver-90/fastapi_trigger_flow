from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from typing import Optional

from src.modules.api_source.api.v1.source.api_source_schemas import DataSourceCreate, DataSourceUpdate
from src.shared.db.models.api_data_source import DataSource


class DataSourceRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: DataSourceCreate) -> DataSource:
        ds = DataSource(**data.dict())
        self.session.add(ds)
        await self.session.commit()
        await self.session.refresh(ds)
        return ds

    async def get(self, source_id: int) -> Optional[DataSource]:
        result = await self.session.execute(select(DataSource).where(DataSource.id == source_id))
        return result.scalar_one_or_none()

    async def list(self, user_id: Optional[int] = None):
        stmt = select(DataSource)
        if user_id:
            stmt = stmt.where(DataSource.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, source_id: int, data: DataSourceUpdate) -> Optional[DataSource]:
        obj = await self.get(source_id)
        if not obj:
            return None
        for key, value in data.dict(exclude_unset=True).items():
            setattr(obj, key, value)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, source_id: int) -> bool:
        obj = await self.get(source_id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True
