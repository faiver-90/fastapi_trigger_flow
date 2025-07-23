from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.base_repo import BaseRepository
from src.shared.db.models.user_notification_bindings import UserNotificationBinding


class NotificationRepo(BaseRepository[UserNotificationBinding]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserNotificationBinding)
