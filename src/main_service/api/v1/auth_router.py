import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.main_service.api.v1.configs.redis_conf import redis_service
from src.main_service.api.v1.schemas import LoginResponseSchema, AuthInSchema, UserOutSchema, UserCreateSchema
from src.main_service.api.v1.services.auth_service import AuthService
from src.main_service.api.v1.services.exceptions_handlers import handle_internal_errors
from src.main_service.db.session import get_async_session
from src.main_service.repositories.jwt_repo import JWTRepo
from src.main_service.repositories.user_repo import UserRepository

v1 = APIRouter()

logger = logging.getLogger(__name__)


@v1.get('/')
async def test_connection():
    return {'It\'s': 'Work'}


@v1.post("/login", response_model=LoginResponseSchema)
@handle_internal_errors()
async def login(token_data: AuthInSchema, db: AsyncSession = Depends(get_async_session)):
    service = AuthService(UserRepository(db), JWTRepo(db), redis_service)

    username = token_data.username

    token_data = await service.login(username, token_data.password)
    return token_data


@v1.post("/register", response_model=UserOutSchema)
@handle_internal_errors()
async def register(data: UserCreateSchema, db: AsyncSession = Depends(get_async_session)):
    service = AuthService(UserRepository(db))
    user = await service.register_user(data)
    return user
