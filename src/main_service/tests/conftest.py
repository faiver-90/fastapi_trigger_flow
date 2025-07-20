from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from passlib.context import CryptContext

from src.main_service.api.v1.services.auth_service import AuthService
from src.main_service.init_app import app

from src.main_service.tests.fake_services.fake_redis import FakeRedis

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(scope="function")
def sync_client():
    return TestClient(app)


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function")
def mock_session():
    return AsyncMock()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
def fake_redis():
    return FakeRedis()


@pytest.fixture
def mock_user_repo():
    return AsyncMock()


@pytest.fixture
def mock_jwt_repo():
    return AsyncMock()


@pytest.fixture
def mock_redis_client():
    return AsyncMock()


@pytest.fixture
def auth_service(mock_user_repo, mock_jwt_repo, mock_redis_client):
    return AuthService(
        user_repo=mock_user_repo,
        jwt_repo=mock_jwt_repo,
        redis_client=mock_redis_client
    )


@pytest.fixture
def mock_user():
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = "testuser"
    mock_user.email = "user@test.com"
    mock_user.hashed_password = pwd_context.hash("correctpassword")
    mock_user.is_superuser = False

    return mock_user
