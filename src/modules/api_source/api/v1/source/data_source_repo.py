from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.shared.base_repo import BaseRepository
from src.shared.db.models.api_data_source import DataSource


class DataSourceRepo(BaseRepository[DataSource]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, DataSource)

    async def list(self, user_id: int | None = None):
        stmt = select(DataSource)
        if user_id:
            stmt = stmt.where(DataSource.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
