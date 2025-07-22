from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.api_source.api.v1.notifications.notification_template_repo import NotificationTemplateRepo
from src.modules.api_source.api.v1.notifications.notification_template_service import CRUDNotificationTemplateService
from src.shared.db.session import get_async_session


async def get_notification_template_service(
        session: AsyncSession = Depends(get_async_session)) -> CRUDNotificationTemplateService:
    repo = NotificationTemplateRepo(session)
    return CRUDNotificationTemplateService(repo)
