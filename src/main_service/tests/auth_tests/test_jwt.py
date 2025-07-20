import pytest

from datetime import timedelta
from jose import jwt, JWTError
from src.main_service.api.v1.schemas import JWTCreateSchema
from src.main_service.api.v1.services.jwt_service import create_token, create_access_token, create_refresh_token, \
    decode_token
from src.main_service.db import RefreshToken
from src.main_service.repositories.jwt_repo import JWTRepo

SECRET_KEY = "secret"
ALGORITHM = "HS256"

TEST_USER_ID = "123"


# JWT repo
@pytest.mark.asyncio
async def test_create_repo_jwt_token(async_mock_session):
    repo = JWTRepo(session=async_mock_session)
    schema = JWTCreateSchema(user_id=1, token="mock_token")

    result = await repo.create(schema)

    assert isinstance(result, RefreshToken)
    assert result.user_id == schema.user_id
    assert result.token == schema.token
    assert not result.revoked

    async_mock_session.add.assert_called_once()
    async_mock_session.commit.assert_called_once()
    async_mock_session.refresh.assert_called_once_with(result)


# JWT service
def test_create_token_contains_exp_and_sub():
    data = {"sub": TEST_USER_ID}
    delta = timedelta(minutes=5)
    token = create_token(data, delta)

    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == TEST_USER_ID
    assert "exp" in decoded
    assert int(decoded["exp"])


def test_create_access_token_valid():
    token = create_access_token(TEST_USER_ID)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == TEST_USER_ID


def test_create_refresh_token_valid():
    token = create_refresh_token(TEST_USER_ID)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == TEST_USER_ID


def test_decode_token_returns_correct_user_id():
    token = create_access_token(TEST_USER_ID)
    result = decode_token(token)
    assert result == TEST_USER_ID


def test_decode_token_with_invalid_signature():
    token = create_access_token(TEST_USER_ID)
    broken_token = token + "abc"

    with pytest.raises(JWTError):
        decode_token(broken_token)


def test_expired_token():
    token = create_token({"sub": TEST_USER_ID}, timedelta(seconds=-1))

    with pytest.raises(JWTError):
        decode_token(token)
