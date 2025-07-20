from datetime import datetime, timedelta

from jose import jwt

from src.shared.configs.jwt_conf import SECRET_KEY, ALGORITHM, ACCESS_EXPIRE_MIN, \
    REFRESH_EXPIRE_DAYS


def create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(user_id: str, **data):
    return create_token({"sub": user_id, **data}, timedelta(minutes=ACCESS_EXPIRE_MIN))


def create_refresh_token(user_id: str, **data):
    return create_token({"sub": user_id, **data}, timedelta(days=REFRESH_EXPIRE_DAYS))


def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
