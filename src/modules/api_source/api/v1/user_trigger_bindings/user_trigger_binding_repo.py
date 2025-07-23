from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.base_repo import BaseRepository
from src.shared.db import UserTriggerBinding


class UserTriggerBindingRepo(BaseRepository[UserTriggerBinding]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserTriggerBinding)
