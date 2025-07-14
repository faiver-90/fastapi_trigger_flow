import pytest

from src.main_service.tests.conftest import client


@pytest.mark.anyio
async def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"It's": 'Work'}

