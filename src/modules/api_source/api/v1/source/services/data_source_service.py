from src.modules.api_source.api.v1.source.data_source_repo import DataSourceRepo
from src.shared.services.base_crud_service import BaseCRUDService
from src.shared.services.fernet_service import FernetService


class CRUDDataSourceService(BaseCRUDService[DataSourceRepo]):
    def __init__(self, repo: DataSourceRepo, fernet: FernetService):
        super().__init__(repo)
        self.fernet = fernet

    async def create(self, data: dict, user_id=None):
        data['source_key'] = self.fernet.encrypt_str(data['source_key'])
        return await super().create(data, user_id)
