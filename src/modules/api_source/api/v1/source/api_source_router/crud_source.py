from fastapi import Depends, HTTPException

from src.shared.deps.auth_dependencies import authenticate_user
from src.modules.api_source.api.v1.source.api_source_schemas import DataSourceOut, DataSourceCreate, DataSourceUpdate
from src.modules.api_source.api.v1.source.get_source_service import get_data_source_service
from src.modules.api_source.api.v1.source.services.data_source_service import CRUDDataSourceService

from fastapi import APIRouter

v1_api_source = APIRouter(prefix="/crud_api_sources", tags=["CRUD API Sources"])


@v1_api_source.post(
    "/",
    response_model=DataSourceOut,
    dependencies=[Depends(authenticate_user)],
    summary="Создание источника данных",
    description="Создаёт новый источник данных с указанными параметрами: имя, учётные данные и статус активности."
)
async def create_api_source(
        data: DataSourceCreate,
        service: CRUDDataSourceService = Depends(get_data_source_service)
):
    return await service.create(data)


@v1_api_source.get(
    "/{source_id}",
    response_model=DataSourceOut,
    dependencies=[Depends(authenticate_user)],
    summary="Получить источник данных",
    description="Возвращает информацию об источнике данных по его ID. Если источник не найден — возвращает ошибку 404."
)
async def get_api_source(
        source_id: int,
        service: CRUDDataSourceService = Depends(get_data_source_service)
):
    result = await service.get(source_id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return result


@v1_api_source.get(
    "/",
    response_model=list[DataSourceOut],
    dependencies=[Depends(authenticate_user)],
    summary="Список источников данных",
    description="Возвращает список всех источников данных. "
                "Можно указать параметр `user_id` для фильтрации по пользователю."
)
async def list_api_sources(
        user_id: int | None = None,
        service: CRUDDataSourceService = Depends(get_data_source_service)
):
    return await service.list(user_id=user_id)


@v1_api_source.put(
    "/{source_id}",
    response_model=DataSourceOut,
    dependencies=[Depends(authenticate_user)],
    summary="Обновить источник данных",
    description="Обновляет данные источника по его ID. Принимает изменённые поля и возвращает обновлённый объект."
                " Ошибка 404, если не найден."
)
async def update_api_source(
        source_id: int,
        data: DataSourceUpdate,
        service: CRUDDataSourceService = Depends(get_data_source_service)
):
    updated = await service.update(source_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Not found")
    return updated


@v1_api_source.delete(
    "/{source_id}",
    dependencies=[Depends(authenticate_user)],
    summary="Удалить источник данных",
    description="Удаляет источник данных по ID. Если источник не найден — возвращает ошибку 404. "
                "Возвращает статус успешного удаления."
)
async def delete_api_source(
        source_id: int,
        service: CRUDDataSourceService = Depends(get_data_source_service)
):
    deleted = await service.delete(source_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Not found")
    return {"status": "deleted"}
