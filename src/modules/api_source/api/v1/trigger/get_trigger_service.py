from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.api_source.api.v1.notifications.notification_repo import NotificationRepo
from src.modules.api_source.api.v1.trigger.trigger_repo import TriggerRepo
from src.modules.api_source.api.v1.trigger.trigger_service import TriggerService
from src.shared.db.session import get_async_session


async def get_trigger_service(session: AsyncSession = Depends(get_async_session)) -> TriggerService:
    trigger_repo = TriggerRepo(session)
    notification_repo = NotificationRepo(session)
    return TriggerService(trigger_repo, notification_repo)
