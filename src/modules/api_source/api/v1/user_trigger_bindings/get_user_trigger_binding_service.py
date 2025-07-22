from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.api_source.api.v1.user_trigger_bindings.user_trigger_binding_repo import UserTriggerBindingRepo
from src.modules.api_source.api.v1.user_trigger_bindings.user_trigger_binding_service import \
    CRUDUserTriggerBindingService
from src.shared.db.session import get_async_session


async def get_user_trigger_binding_service(
        session: AsyncSession = Depends(get_async_session)) -> CRUDUserTriggerBindingService:
    repo = UserTriggerBindingRepo(session)
    return CRUDUserTriggerBindingService(repo)
