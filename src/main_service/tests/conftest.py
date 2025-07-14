import pytest
from fastapi.testclient import TestClient

from src.main_service.init_app import app

from src.main_service.tests.fake_services.fake_redis import FakeRedis

client = TestClient(app)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
def fake_redis():
    return FakeRedis()

# @pytest.fixture
# def my_service(fake_redis):
#     from my_app.services import MyService
#     return MyService(redis_client=fake_redis)
