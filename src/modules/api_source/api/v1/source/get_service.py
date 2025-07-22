from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.api_source.api.v1.source.services.data_source_service import CRUDDataSourceService
from src.modules.api_source.api.v1.source.data_source_repo import DataSourceRepo
from src.shared.db.session import get_async_session
from src.shared.services.fernet_service import FernetService


async def get_data_source_service(session: AsyncSession = Depends(get_async_session)) -> CRUDDataSourceService:
    """
    Провайдер зависимости для CRUD-сервиса источников данных.

    Создаёт и возвращает экземпляр `CRUDDataSourceService`, который инкапсулирует
    бизнес-логику для работы с моделью `DataSource`, используя переданную сессию БД
    и сервис шифрования `FernetService`.

    Используется как зависимость (`Depends`) в маршрутах FastAPI.

    Параметры:
        session (AsyncSession): Асинхронная сессия SQLAlchemy, полученная через Depends.

    Возвращает:
        CRUDDataSourceService: Сервис для операций создания, чтения, обновления и удаления источников данных.
    """
    repo = DataSourceRepo(session)
    fernet = FernetService()
    return CRUDDataSourceService(repo, fernet)
