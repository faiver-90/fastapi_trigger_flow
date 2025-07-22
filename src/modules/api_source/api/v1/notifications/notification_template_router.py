from fastapi import Depends, HTTPException, APIRouter

from src.modules.api_source.api.v1.notifications.get_notification_template_service import \
    get_notification_template_service
from src.modules.api_source.api.v1.notifications.notification_template_schemas import NotificationTemplateOut, \
    NotificationTemplateCreate, NotificationTemplateUpdate
from src.modules.api_source.api.v1.notifications.notification_template_service import CRUDNotificationTemplateService
from src.shared.deps.auth_dependencies import verify_superuser

v1_notification_router = APIRouter(
    prefix="/notification_template",
    tags=["Notification Templates"],
    dependencies=[Depends(verify_superuser)]
)


@v1_notification_router.post(
    "/", response_model=NotificationTemplateOut,
    summary="Создание notification template",
    description="Создаёт новый notification template на основе входных данных."
)
async def create_notification_template(
        data: NotificationTemplateCreate,
        service: CRUDNotificationTemplateService = Depends(get_notification_template_service)):
    return await service.create(data.dict())


@v1_notification_router.get(
    "/{item_id}",
    response_model=NotificationTemplateOut,
    summary="Получение notification template по ID",
    description="Возвращает notification template по ID. Возвращает ошибку 404, если не найден."
)
async def get_notification_template(
        item_id: int,
        service: CRUDNotificationTemplateService = Depends(get_notification_template_service)):
    obj = await service.get(item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@v1_notification_router.get(
    "/",
    response_model=list[NotificationTemplateOut],
    summary="Получение notification template по ID",
    description="Возвращает notification template по ID. Возвращает ошибку 404, если не найден."
)
async def list_notification_templates(
        service: CRUDNotificationTemplateService = Depends(get_notification_template_service)):
    return await service.list()


@v1_notification_router.put(
    "/{item_id}",
    response_model=NotificationTemplateOut,
    summary="Обновление notification template",
    description="Обновляет notification template по ID. Возвращает ошибку 404, если не найден."
)
async def update_notification_template(
        item_id: int, data: NotificationTemplateUpdate,
        service: CRUDNotificationTemplateService = Depends(
            get_notification_template_service)):
    obj = await service.update(item_id, data.dict(exclude_unset=True))
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@v1_notification_router.delete(
    "/{item_id}",
    summary="Удаление notification template",
    description="Удаляет notification template по ID. Возвращает ошибку 404, если не найден."
)
async def delete_notification_template(
        item_id: int,
        service: CRUDNotificationTemplateService = Depends(get_notification_template_service)):
    deleted = await service.delete(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Not found")
    return {"status": "deleted"}
