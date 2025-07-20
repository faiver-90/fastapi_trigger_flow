from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from passlib.context import CryptContext

from src.main_service.api.v1.services.auth_service import AuthService
from src.main_service.api.v1.services.stream_exceptions_handlers import validation_exception_handler, \
    http_exception_handler, generic_exception_handler
from src.main_service.db import User
from src.main_service.repositories.user_repo import UserRepository

from src.main_service.tests.fake_services.fake_redis import FakeRedis

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(scope="function")
def test_app():
    app = FastAPI()

    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    @app.get("/validation-error")
    async def validation_route(limit: int):
        return {"limit": limit}

    @app.get("/http-error")
    async def http_error_route():
        raise HTTPException(status_code=403, detail="Forbidden action")

    @app.get("/unexpected-error")
    async def unexpected_route():
        raise RuntimeError("Something went wrong")

    @app.get("/")
    async def root():
        return {"It's": "Work"}

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


@pytest.fixture(scope="function")
def fake_redis():
    return FakeRedis()


@pytest.fixture(scope="function")
def mock_user_repo():
    return AsyncMock()


@pytest.fixture(scope="function")
def mock_jwt_repo():
    return AsyncMock()


@pytest.fixture(scope="function")
def mock_redis_client():
    return AsyncMock()


@pytest.fixture(scope="function")
def auth_service(mock_user_repo, mock_jwt_repo, mock_redis_client):
    return AuthService(
        user_repo=mock_user_repo,
        jwt_repo=mock_jwt_repo,
        redis_client=mock_redis_client
    )


@pytest.fixture(scope="function")
def mock_user():
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = "testuser"
    mock_user.email = "user@test.com"
    mock_user.hashed_password = pwd_context.hash("correctpassword")
    mock_user.is_superuser = False

    return mock_user


@pytest.fixture(scope="function")
def user_repo(async_mock_session):
    return UserRepository(session=async_mock_session)


@pytest.fixture(scope="function")
def fake_user():
    return User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed123"
    )
