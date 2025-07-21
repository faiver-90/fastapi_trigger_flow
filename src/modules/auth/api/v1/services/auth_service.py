import logging

from src.modules.auth.api.v1.services.jwt_service import create_access_token, create_refresh_token

from src.modules.auth.api.v1.schemas import JWTCreateSchema, LoginResponseSchema, UserOutSchema, UserCreateSchema
from src.modules.auth.configs.crypt_conf import pwd_context
from src.modules.auth.configs.jwt_conf import ACCESS_EXPIRE_MIN
from src.modules.auth.configs.log_conf import setup_auth_logger
from src.modules.auth.repositories.jwt_repo import JWTRepo
from src.modules.auth.repositories.user_repo import UserRepository
from src.modules.auth.api.v1.services.redis_service import RedisService

setup_auth_logger()
auth_logger = logging.getLogger('auth')
errors_logger = logging.getLogger('errors')


class AuthService:
    """
    Сервис авторизации пользователей. Отвечает за вход, регистрацию, генерацию токенов и их сохранение.
    """
    def __init__(self,
                 user_repo: UserRepository = None, jwt_repo: JWTRepo = None, redis_client: RedisService = None):
        """
        Инициализация сервиса.

        Args:
            user_repo (UserRepository): Репозиторий пользователей.
            jwt_repo (JWTRepo): Репозиторий JWT токенов.
            redis_client (RedisService): Клиент Redis для хранения access токенов.
       """
        self.user_repo = user_repo
        self.jwt_repo = jwt_repo
        self.redis_client = redis_client

    async def login(self, username: str, password: str):
        """
        Аутентификация пользователя и выдача JWT токенов.

        Args:
            username (str): Имя пользователя.
            password (str): Пароль.

        Returns:
            LoginResponseSchema: JWT токены и информация о пользователе.

        Raises:
            ValueError: Если логин или пароль неверные.
        """
        user = await self.user_repo.get_by_fields(username=username)

        if not user or not pwd_context.verify(password, user.hashed_password):
            auth_logger.info(f"User {username} unsuccessfully logged in")
            errors_logger.error(f"Invalid username or password {username}")
            raise ValueError("Invalid username or password")

        user_id = str(user.id)
        jwt_data = {
            "is_superuser": user.is_superuser
        }

        access = create_access_token(user_id, **jwt_data)
        refresh = create_refresh_token(user_id, **jwt_data)

        await self.redis_client.set(user_id, access, 60 * ACCESS_EXPIRE_MIN)

        jwt = await self.jwt_repo.create(JWTCreateSchema(user_id=user_id, token=refresh))

        return LoginResponseSchema(
            access_token=access,
            refresh_token=refresh,
            token_type="bearer",
            expires_at=jwt.expires_at,
            user=UserOutSchema(
                id=user_id,
                username=username,
                email=user.email,
                is_superuser=user.is_superuser
            )
        )

    async def register_user(self, data: UserCreateSchema):
        """
        Регистрация нового пользователя.

        Args:
            data (UserCreateSchema): Данные для создания пользователя.

        Returns:
            User: Созданный пользователь.

        Raises:
            ValueError: Если пользователь с таким email или username уже существует.
        """
        existing_user = await self.user_repo.exists_by_fields(email=data.email, username=data.username)
        if existing_user:
            auth_logger.info(f"User with this {data.email} or {data.username} already exists")
            raise ValueError("User with this email or username already exists")

        hashed_password = pwd_context.hash(data.password)
        return await self.user_repo.create(data, hashed_password)
