from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(scope="function")
def test_app():
    app = FastAPI()

    return app


@pytest.fixture(scope="function")
def sync_client(test_app):
    return TestClient(test_app, raise_server_exceptions=False)


@pytest.fixture(scope="function")
async def async_client(test_app):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function")
def mock_result():
    return MagicMock()


@pytest.fixture(scope="function")
def async_mock_session():
    return AsyncMock()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"
#
#
# @pytest.fixture(scope="function")
# def fake_redis():
#     return FakeRedis()


@pytest.fixture(scope="function")
def mock_redis_client():
    return AsyncMock()


@pytest.fixture(scope="function")
def mock_user():
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = "testuser"
    mock_user.email = "user@test.com"
    mock_user.hashed_password = pwd_context.hash("correctpassword")
    mock_user.is_superuser = False

    return mock_user
