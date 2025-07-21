from src.modules.api_source.repositories.data_source_repo import DataSourceRepo
from src.modules.api_source.api.v1.schemas import DataSourceCreate, DataSourceUpdate


class CRUDDataSourceService:
    def __init__(self, repo: DataSourceRepo):
        self.repo = repo

    async def create(self, data: DataSourceCreate):
        return await self.repo.create(data)

    async def get(self, source_id: int):
        return await self.repo.get(source_id)

    async def list(self, user_id: int | None = None):
        return await self.repo.list(user_id=user_id)

    async def update(self, source_id: int, data: DataSourceUpdate):
        return await self.repo.update(source_id, data)

    async def delete(self, source_id: int):
        return await self.repo.delete(source_id)
