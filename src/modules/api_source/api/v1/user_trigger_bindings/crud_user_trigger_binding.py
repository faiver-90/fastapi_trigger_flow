from fastapi import Depends, HTTPException, APIRouter
from src.shared.deps.auth_dependencies import authenticate_user
from src.modules.api_source.api.v1.user_trigger_bindings.get_user_trigger_binding_service import \
    get_user_trigger_binding_service
from src.modules.api_source.api.v1.user_trigger_bindings.user_trigger_binding_schemas import UserTriggerBindingCreate, \
    UserTriggerBindingOut, UserTriggerBindingUpdate
from src.modules.api_source.api.v1.user_trigger_bindings.user_trigger_binding_service import \
    CRUDUserTriggerBindingService

v1_user_trigger_binding_router = APIRouter(
    prefix="/user_trigger_binding",
    tags=["User Trigger Bindings"],
    dependencies=[Depends(authenticate_user)]
)


@v1_user_trigger_binding_router.post(
    "/",
    response_model=UserTriggerBindingOut,
    dependencies=[Depends(authenticate_user)],
    summary="Создание привязки триггера к пользователю",
    description="Создаёт новый привязки триггера к пользователю на основе входных данных."
)
async def create_user_trigger_binding(data: UserTriggerBindingCreate,
                                      service: CRUDUserTriggerBindingService = Depends(
                                          get_user_trigger_binding_service)):
    return await service.create(data.dict())


@v1_user_trigger_binding_router.get(
    "/{item_id}",
    response_model=UserTriggerBindingOut,
    dependencies=[Depends(authenticate_user)],
    summary="Получение привязки триггера к пользователю по ID",
    description="Возвращает привязки триггера к пользователю по ID. Возвращает ошибку 404, если не найден."
)
async def get_user_trigger_binding(
        item_id: int,
        service: CRUDUserTriggerBindingService = Depends(get_user_trigger_binding_service)
):
    obj = await service.get(item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@v1_user_trigger_binding_router.get(
    "/",
    response_model=list[UserTriggerBindingOut],
    dependencies=[Depends(authenticate_user)],
    summary="Получение привязки триггера к пользователю по ID",
    description="Возвращает привязки триггера к пользователю по ID. Возвращает ошибку 404, если не найден."
)
async def list_user_trigger_bindings(
        service: CRUDUserTriggerBindingService = Depends(get_user_trigger_binding_service)):
    return await service.list()


@v1_user_trigger_binding_router.put(
    "/{item_id}",
    response_model=UserTriggerBindingOut,
    dependencies=[Depends(authenticate_user)],
    summary="Обновление привязки триггера к пользователю",
    description="Обновляет привязки триггера к пользователю по ID. Возвращает ошибку 404, если не найден."
)
async def update_user_trigger_binding(
        item_id: int, data: UserTriggerBindingUpdate,
        service: CRUDUserTriggerBindingService = Depends(get_user_trigger_binding_service)):
    obj = await service.update(item_id, data.dict(exclude_unset=True))
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@v1_user_trigger_binding_router.delete(
    "/{item_id}",
    dependencies=[Depends(authenticate_user)],
    summary="Удаление привязки триггера к пользователю",
    description="Удаляет привязки триггера к пользователю по ID. Возвращает ошибку 404, если не найден."
)
async def delete_user_trigger_binding(
        item_id: int,
        service: CRUDUserTriggerBindingService = Depends(get_user_trigger_binding_service)):
    deleted = await service.delete(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Not found")
    return {"status": "deleted"}
