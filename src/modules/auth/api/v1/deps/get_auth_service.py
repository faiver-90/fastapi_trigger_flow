from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.api.v1.services.auth_service import AuthService
from src.modules.auth.repositories.jwt_repo import JWTRepo
from src.modules.auth.repositories.user_repo import UserRepository
from src.shared.db.session import get_async_session
from src.shared.services.redis_service import redis_service


def get_auth_service(db: AsyncSession = Depends(get_async_session)) -> AuthService:
    """
    Провайдер зависимостей для получения экземпляра AuthService с необходимыми репозиториями.

    Args:
        db (AsyncSession): Асинхронная сессия базы данных, предоставляется через Depends.

    Returns:
        AuthService: Экземпляр сервиса авторизации.
    """
    return AuthService(
        user_repo=UserRepository(db), jwt_repo=JWTRepo(db), redis_client=redis_service
    )
