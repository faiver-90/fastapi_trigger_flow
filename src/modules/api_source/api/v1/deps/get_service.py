from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.api_source.api.v1.services.data_source_service import CRUDDataSourceService
from src.modules.api_source.repositories.data_source_repo import DataSourceRepo
from src.shared.db.session import get_async_session
from src.shared.services.fernet_service import FernetService


async def get_data_source_service(session: AsyncSession = Depends(get_async_session)) -> CRUDDataSourceService:
    repo = DataSourceRepo(session)
    fernet = FernetService()
    return CRUDDataSourceService(repo, fernet)
