from fastapi import Depends, HTTPException, APIRouter

from src.modules.api_source.api.v1.notifications.get_notification_service import \
    get_notification_service
from src.modules.api_source.api.v1.notifications.notification_schemas import NotificationOut, \
    NotificationCreate, NotificationUpdate
from src.modules.api_source.api.v1.notifications.notification_service import CRUDNotificationService
from src.shared.deps.auth_dependencies import authenticate_user

v1_notification_router = APIRouter(
    prefix="/notification",
    tags=["Notification"],
    dependencies=[Depends(authenticate_user)]
)


@v1_notification_router.post(
    "/", response_model=NotificationOut,
    summary="Создание notification",
    description="Создаёт новый notification  на основе входных данных."
)
async def create_notification(
        data: NotificationCreate,
        service: CRUDNotificationService = Depends(get_notification_service)):
    return await service.create(data.dict())


@v1_notification_router.get(
    "/{item_id}",
    response_model=NotificationOut,
    summary="Получение notification по ID",
    description="Возвращает notification по ID. Возвращает ошибку 404, если не найден."
)
async def get_notification(
        item_id: int,
        service: CRUDNotificationService = Depends(get_notification_service)):
    obj = await service.get(item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@v1_notification_router.get(
    "/",
    response_model=list[NotificationOut],
    summary="Получение notification по ID",
    description="Возвращает notification по ID. Возвращает ошибку 404, если не найден."
)
async def list_notification(
        service: CRUDNotificationService = Depends(get_notification_service)):
    return await service.list()


@v1_notification_router.put(
    "/{item_id}",
    response_model=NotificationOut,
    summary="Обновление notification",
    description="Обновляет notification по ID. Возвращает ошибку 404, если не найден."
)
async def update_notification(
        item_id: int, data: NotificationUpdate,
        service: CRUDNotificationService = Depends(
            get_notification_service)):
    obj = await service.update(item_id, data.dict(exclude_unset=True))
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@v1_notification_router.delete(
    "/{item_id}",
    summary="Удаление notification",
    description="Удаляет notification по ID. Возвращает ошибку 404, если не найден."
)
async def delete_notification(
        item_id: int,
        service: CRUDNotificationService = Depends(get_notification_service)):
    deleted = await service.delete(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Not found")
    return {"status": "deleted"}
