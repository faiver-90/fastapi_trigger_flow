from src.modules.api_source.api.v1.source.data_source_repo import DataSourceRepo
from src.modules.api_source.api.v1.source.api_source_schemas import DataSourceCreate, DataSourceUpdate
from src.shared.services.fernet_service import FernetService


class CRUDDataSourceService:
    def __init__(self, repo: DataSourceRepo, fernet: FernetService):
        self.repo = repo
        self.fernet = fernet

    async def create(self, data: DataSourceCreate):
        data.source_key = self.fernet.encrypt_str(data.source_key)
        return await self.repo.create(data)

    async def get(self, source_id: int):
        return await self.repo.get(source_id)

    async def list(self, user_id: int | None = None):
        return await self.repo.list(user_id=user_id)

    async def update(self, source_id: int, data: DataSourceUpdate):
        return await self.repo.update(source_id, data)

    async def delete(self, source_id: int):
        return await self.repo.delete(source_id)
