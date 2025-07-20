import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.api.v1.schemas import LoginResponseSchema, AuthInSchema, UserOutSchema, UserCreateSchema
from src.modules.auth.api.v1.services.auth_service import AuthService
from src.modules.auth.api.v1.services.redis_service import redis_service
from src.modules.auth.configs.log_conf import setup_auth_logger
from src.modules.auth.exceptions_handle.exceptions_handlers import handle_internal_errors
from src.shared.db.session import get_async_session
from src.modules.auth.repositories.jwt_repo import JWTRepo
from src.modules.auth.repositories.user_repo import UserRepository

v1 = APIRouter()

setup_auth_logger()
auth_logger = logging.getLogger('auth')


@v1.post(
    "/login",
    response_model=LoginResponseSchema,
    summary="Вход пользователя",
    description="Авторизация по имени пользователя и паролю. Возвращает JWT токен и информацию о пользователе.",
    tags=["Аутентификация"]
)
@handle_internal_errors()
async def login(token_data: AuthInSchema, db: AsyncSession = Depends(get_async_session)):
    service = AuthService(UserRepository(db), JWTRepo(db), redis_service)
    username = token_data.username
    token_data = await service.login(username, token_data.password)
    auth_logger.info(f"User '{username}' successfully logged in")

    return token_data


@v1.post(
    "/register",
    response_model=UserOutSchema,
    summary="Регистрация нового пользователя",
    description="Регистрирует нового пользователя с заданными email, username и паролем. "
                "Возвращает данные пользователя.",
    tags=["Аутентификация"]
)
@handle_internal_errors()
async def register(data: UserCreateSchema, db: AsyncSession = Depends(get_async_session)):
    service = AuthService(UserRepository(db))
    user = await service.register_user(data)
    auth_logger.info("New user registered: username=%s, email=%s", data.username, data.email)

    return user
