from datetime import datetime, timedelta

from jose import jwt

from src.modules.auth.configs.jwt_conf import SECRET_KEY, ALGORITHM, ACCESS_EXPIRE_MIN, \
    REFRESH_EXPIRE_DAYS


def create_token(data: dict, expires_delta: timedelta) -> str:
    """
    Создать JWT токен.

    Args:
        data (dict): Данные для включения в токен.
        expires_delta (timedelta): Время жизни токена.

    Returns:
        str: JWT токен.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(user_id: str, **data):
    """
    Создать access токен.

    Args:
        user_id (str): Идентификатор пользователя.
        **data: Дополнительные данные (например, is_superuser).

    Returns:
        str: Access токен.
    """

    return create_token({"sub": user_id, **data}, timedelta(minutes=ACCESS_EXPIRE_MIN))


def create_refresh_token(user_id: str, **data):
    """
    Создать refresh токен.

    Args:
        user_id (str): Идентификатор пользователя.
        **data: Дополнительные данные.

    Returns:
        str: Refresh токен.
    """
    return create_token({"sub": user_id, **data}, timedelta(days=REFRESH_EXPIRE_DAYS))


def decode_token(token: str):
    """
    Расшифровать и проверить JWT токен.

    Args:
        token (str): JWT токен.

    Returns:
        dict: Расшифрованные данные.

    Raises:
        JWTError: Если токен недействителен или истёк.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
