import logging

from fastapi import APIRouter, Depends, HTTPException

from src.modules.auth.api.v1.deps.get_auth_service import get_auth_service
from src.modules.auth.api.v1.schemas import LoginResponseSchema, AuthInSchema, UserOutSchema, UserCreateSchema
from src.modules.auth.api.v1.services.auth_service import AuthService
from src.modules.auth.configs.log_conf import setup_auth_logger

v1_auth = APIRouter(prefix="/auth", tags=["Authentication, authorisation"])

setup_auth_logger()
auth_logger = logging.getLogger('auth')


@v1_auth.post(
    "/login",
    response_model=LoginResponseSchema,
    summary="Вход пользователя",
    description="Авторизация по имени пользователя и паролю. Возвращает JWT токен и информацию о пользователе."
)
async def login(
        token_data: AuthInSchema,
        service: AuthService = Depends(get_auth_service)
):
    try:
        username = token_data.username
        token_data = await service.login(username, token_data.password)
        auth_logger.info(f"User '{username}' successfully logged in")

        return token_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


@v1_auth.post(
    "/register",
    response_model=UserOutSchema,
    summary="Регистрация нового пользователя",
    description="Регистрирует нового пользователя с заданными email, username и паролем. "
                "Возвращает данные пользователя."
)
async def register(
        data: UserCreateSchema,
        service: AuthService = Depends(get_auth_service)
):
    try:
        user = await service.register_user(data)
        auth_logger.info("New user registered: username=%s, email=%s", data.username, data.email)

        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
