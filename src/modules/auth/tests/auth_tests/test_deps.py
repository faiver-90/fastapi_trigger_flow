from datetime import timedelta

from src.modules.auth.api.v1.services.jwt_service import create_token


def test_authenticate_user_valid_token(sync_client):
    token = create_token(
        {"sub": "1", "username": "test", "is_superuser": False}, timedelta(minutes=15)
    )
    response = sync_client.get(
        "/auth-only", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["user"]["sub"] == "1"
    assert response.json()["user"]["is_superuser"] is False


def test_authenticate_user_invalid_token(sync_client):
    response = sync_client.get(
        "/auth-only", headers={"Authorization": "Bearer invalid.token.here"}
    )
    assert response.status_code == 401
    assert "Invalid token" in response.json()["message"]


def test_authenticate_user_no_token(sync_client):
    response = sync_client.get("/auth-only")
    assert response.status_code == 403


def test_verify_superuser_valid(sync_client):
    token = create_token(
        {"sub": "1", "username": "test", "is_superuser": True}, timedelta(minutes=15)
    )
    response = sync_client.get(
        "/superuser-only", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["user"]["is_superuser"] is True


def test_verify_superuser_invalid(sync_client):
    token = create_token(
        {"sub": "1", "username": "test", "is_superuser": False}, timedelta(minutes=15)
    )
    response = sync_client.get(
        "/superuser-only", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
    assert response.json()["message"] == "User is not a superuser"
