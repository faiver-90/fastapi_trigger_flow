import logging

from api.v1.configs.crypt_conf import pwd_context
from api.v1.configs.jwt_conf import ACCESS_EXPIRE_MIN
from api.v1.schemas import JWTCreateSchema, UserOutSchema, TokenResponseSchema, \
    UserCreateSchema
from api.v1.services.jwt_service import create_access_token, \
    create_refresh_token
from api.v1.services.redis_service import RedisService
from repositories.jwt_repo import JWTRepo
from repositories.user_repo import UserRepository

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self,
                 user_repo: UserRepository = None,
                 jwt_repo: JWTRepo = None,
                 redis_service: RedisService = None):
        self.user_repo = user_repo
        self.jwt_repo = jwt_repo
        self.redis_service = redis_service

    async def login(self, username: str, password: str, chat_id: str):
        user = await self.user_repo.get_by_fields(username=username)
        if not user:
            logger.error(f'Invalid username or password. Username - '
                         f'{username}')
            raise ValueError("Invalid username or password")

        if not pwd_context.verify(password, user.hashed_password):
            logger.error(f'Invalid username or password. Username - '
                         f'{username}')
            raise ValueError("Invalid username or password")

        access = create_access_token(user.username)
        refresh = create_refresh_token(user.username)

        if not await self.redis_service.get_auth_token(chat_id):
            await self.redis_service.save_auth_token(chat_id,
                                                     access,
                                                     60 * ACCESS_EXPIRE_MIN)

        jwt = await self.jwt_repo.create(JWTCreateSchema(user_id=user.id,
                                                         token=refresh))
        return TokenResponseSchema(
            access_token=access,
            refresh_token=refresh,
            token_type="bearer",
            expires_at=jwt.expires_at,
            user=UserOutSchema(
                id=user.id,
                username=user.username,
                email=user.email,
                is_superuser=user.is_superuser
            )
        )

    async def register_user(self, data: UserCreateSchema):
        existing_user = await self.user_repo.exists_by_fields(
            email=data.email,
            username=data.username)
        if existing_user:
            raise ValueError("User with this email or username already exists")

        hashed_password = pwd_context.hash(data.password)
        return await self.user_repo.create(data, hashed_password)
