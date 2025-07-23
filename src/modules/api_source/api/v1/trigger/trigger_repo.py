from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.base_repo import BaseRepository
from src.shared.db.models.user_trigger_bindings import UserTriggerBinding


class TriggerRepo(BaseRepository[UserTriggerBinding]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserTriggerBinding)
