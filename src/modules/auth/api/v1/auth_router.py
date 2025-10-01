import logging

from fastapi import APIRouter, Depends, HTTPException

from src.modules.auth.api.v1.deps.get_auth_service import get_auth_service
from src.modules.auth.api.v1.schemas import (
    AuthInSchema,
    LoginResponseSchema,
    UserCreateSchema,
    UserOutSchema,
)
from src.modules.auth.api.v1.services.auth_service import AuthService
from src.shared.decorators import log_action
from src.shared.deps.auth_dependencies import authenticate_user

v1_auth = APIRouter(prefix="/auth", tags=["Authentication, authorisation"])

auth_logger = logging.getLogger("auth_log")


@v1_auth.get("/me", summary="Получить данные текущего пользователя")
async def get_current_user(payload: dict = Depends(authenticate_user)):
    return {
        "user_id": payload.get("sub"),
        "is_superuser": payload.get("is_superuser"),
    }


@v1_auth.post(
    "/login",
    response_model=LoginResponseSchema,
    summary="Вход пользователя",
    description="Авторизация по имени пользователя и паролю. Возвращает JWT токен и информацию о пользователе.",
)
@log_action("User {username} successfully logged in", auth_logger)
async def login(
    token_data: AuthInSchema, service: AuthService = Depends(get_auth_service)
):
    try:
        username = token_data.username
        login_response = await service.login(username, token_data.password)
        return login_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}") from e


@v1_auth.post(
    "/register",
    response_model=UserOutSchema,
    summary="Регистрация нового пользователя",
    description="Регистрирует нового пользователя с заданными email, username и паролем. "
    "Возвращает данные пользователя.",
)
@log_action("New user registered: {username}, {email}", auth_logger)
async def register(
    data: UserCreateSchema, service: AuthService = Depends(get_auth_service)
):
    try:
        user = await service.register_user(data)

        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}") from e
