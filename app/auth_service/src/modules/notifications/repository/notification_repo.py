from sqlalchemy.ext.asyncio import AsyncSession

from app.auth_service.src.shared.base_repo import BaseRepository
from app.auth_service.src.shared.db.models.notifications import Notifications


class NotificationRepo(BaseRepository[Notifications]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Notifications)
