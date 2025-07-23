from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.base_repo import BaseRepository
from src.shared.db import NotificationTemplate


class NotificationTemplateRepo(BaseRepository[NotificationTemplate]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, NotificationTemplate)
