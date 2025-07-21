from datetime import timedelta, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.api.v1.schemas import JWTCreateSchema
from src.modules.auth.configs.jwt_conf import REFRESH_EXPIRE_DAYS
from src.shared.db.models.auth import RefreshToken


class JWTRepo:
    """
    Репозиторий для работы с refresh токенами в базе данных.
    """
    def __init__(self, session: AsyncSession):
        """
        Инициализация сессии SQLAlchemy.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.
        """
        self.session = session

    async def create(self, jwt_data: JWTCreateSchema):
        """
        Создать и сохранить refresh токен.

        Args:
            jwt_data (JWTCreateSchema): Данные токена.

        Returns:
            RefreshToken: Созданный токен.
        """
        expires_at = datetime.utcnow() + timedelta(days=REFRESH_EXPIRE_DAYS)

        jwt = RefreshToken(user_id=jwt_data.user_id, token=jwt_data.token, expires_at=expires_at, revoked=False)

        self.session.add(jwt)
        await self.session.commit()
        await self.session.refresh(jwt)

        return jwt
