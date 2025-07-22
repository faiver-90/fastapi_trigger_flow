from fastapi import Depends, HTTPException, APIRouter

from src.modules.api_source.api.v1.trigger.trigger_types.registered_trigger import TRIGGER_REGISTRY
from src.shared.deps.auth_dependencies import verify_superuser
from src.modules.api_source.api.v1.trigger.get_trigger_service import get_trigger_service
from src.modules.api_source.api.v1.trigger.trigger_schemas import TriggerCreate, TriggerOut, TriggerUpdate
from src.modules.api_source.api.v1.trigger.trigger_service import CRUDTriggerService

v1_trigger_router = APIRouter(
    prefix="/trigger",
    tags=["Triggers"]
)


@v1_trigger_router.get(
    "/list_types",
    dependencies=[],
    summary="Список доступных типов триггеров",
    description="Возвращает список всех зарегистрированных типов триггеров и схемы параметров для каждого."
)
async def list_trigger_types():
    return [
        {
            "name": name,
            "condition": trigger.describe()
        }
        for name, trigger in TRIGGER_REGISTRY.items()
    ]


@v1_trigger_router.post(
    "/", response_model=TriggerOut,
    dependencies=[Depends(verify_superuser)],
    summary="Создание триггера",
    description="Создаёт новый триггера на основе входных данных."
)
async def create_trigger(data: TriggerCreate, service: CRUDTriggerService = Depends(get_trigger_service)):
    return await service.create(data.dict())


@v1_trigger_router.get(
    "/{item_id}",
    response_model=TriggerOut,
    dependencies=[Depends(verify_superuser)],
    summary="Получение триггера по ID",
    description="Возвращает триггера по ID. Возвращает ошибку 404, если не найден."
)
async def get_trigger(item_id: int, service: CRUDTriggerService = Depends(get_trigger_service)):
    obj = await service.get(item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@v1_trigger_router.get(
    "/", response_model=list[TriggerOut],
    dependencies=[Depends(verify_superuser)],
    summary="Получение триггера по ID",
    description="Возвращает триггера по ID. Возвращает ошибку 404, если не найден."
)
async def list_triggers(service: CRUDTriggerService = Depends(get_trigger_service)):
    return await service.list()


@v1_trigger_router.put(
    "/{item_id}",
    response_model=TriggerOut,
    dependencies=[Depends(verify_superuser)],
    summary="Обновление триггера",
    description="Обновляет триггера по ID. Возвращает ошибку 404, если не найден."
)
async def update_trigger(item_id: int, data: TriggerUpdate, service: CRUDTriggerService = Depends(get_trigger_service)):
    obj = await service.update(item_id, data.dict(exclude_unset=True))
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@v1_trigger_router.delete(
    "/{item_id}",
    dependencies=[Depends(verify_superuser)],
    summary="Удаление триггера",
    description="Удаляет триггера по ID. Возвращает ошибку 404, если не найден.")
async def delete_trigger(item_id: int, service: CRUDTriggerService = Depends(get_trigger_service)):
    deleted = await service.delete(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Not found")
    return {"status": "deleted"}
