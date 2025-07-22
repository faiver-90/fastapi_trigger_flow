import pytest

from src.modules.auth.api.v1.schemas import UserCreateSchema, LoginResponseSchema
from unittest.mock import AsyncMock

from src.shared.db.models.auth import User


@pytest.mark.anyio
async def test_health_check(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"It's": 'Work'}


# Auth service
@pytest.mark.asyncio
async def test_login_success(auth_service, mock_user_repo, mock_jwt_repo, mock_redis_client, mock_user):
    mock_user_repo.get_by_fields.return_value = mock_user
    mock_jwt_repo.create.return_value.expires_at = "2030-01-01T00:00:00"

    response = await auth_service.login("testuser", "correctpassword")

    assert isinstance(response, LoginResponseSchema)
    assert response.user.username == "testuser"
    assert response.token_type == "bearer"
    mock_redis_client.set.assert_called_once()
    mock_jwt_repo.create.assert_called_once()


@pytest.mark.asyncio
async def test_login_wrong_password(auth_service, mock_user_repo, mock_user):
    mock_user_repo.get_by_fields.return_value = mock_user

    with pytest.raises(ValueError, match="Invalid username or password"):
        await auth_service.login("testuser", "wrongpassword")


@pytest.mark.asyncio
async def test_login_user_not_found(auth_service, mock_user_repo):
    mock_user_repo.get_by_fields.return_value = None

    with pytest.raises(ValueError, match="Invalid username or password"):
        await auth_service.login("notfound", "any")


@pytest.mark.asyncio
async def test_register_user_success(auth_service, mock_user_repo, mock_user):
    data = UserCreateSchema(
        username=mock_user.username,
        email=mock_user.email,
        password="securepassword"
    )

    mock_user_repo.exists_by_fields.return_value = False
    mock_user_repo.create.return_value = "UserObject"

    result = await auth_service.register_user(data)

    assert result == "UserObject"
    mock_user_repo.create.assert_called_once()


@pytest.mark.asyncio
async def test_register_user_already_exists(auth_service, mock_user_repo, mock_user):
    data = UserCreateSchema(
        username=mock_user.username,
        email=mock_user.email,
        password="123456"
    )
    mock_user_repo.exists_by_fields.return_value = True

    with pytest.raises(ValueError, match="User with this email or username already exists"):
        await auth_service.register_user(data)


# Auth repo
@pytest.mark.anyio
async def test_get_by_fields_found(user_repo, async_mock_session, fake_user, mock_result):
    mock_result.scalar_one_or_none.return_value = fake_user
    async_mock_session.execute.return_value = mock_result

    result = await user_repo.get_by_fields(username="testuser")

    async_mock_session.execute.assert_called_once()
    assert result == fake_user


@pytest.mark.anyio
async def test_get_by_fields_not_found(user_repo, async_mock_session, mock_result):
    mock_result.scalar_one_or_none.return_value = None
    async_mock_session.execute.return_value = mock_result

    result = await user_repo.get_by_fields(email="nope@example.com")

    async_mock_session.execute.assert_called_once()
    assert result is None


@pytest.mark.anyio
async def test_exists_by_fields_true(user_repo, async_mock_session, mock_result):
    mock_result.scalar.return_value = True
    async_mock_session.execute.return_value = mock_result

    result = await user_repo.exists_by_fields(username="testuser")

    async_mock_session.execute.assert_called_once()
    assert result is True


@pytest.mark.anyio
async def test_exists_by_fields_false(user_repo, async_mock_session, mock_result):
    mock_result.scalar.return_value = False
    async_mock_session.execute.return_value = mock_result

    result = await user_repo.exists_by_fields(email="missing@example.com")

    async_mock_session.execute.assert_called_once()
    assert result is False


# @pytest.mark.anyio
# async def test_update_user_by_id(user_repo, async_mock_session):
#     data = {"email": "new@example.com"}
#
#     await user_repo.update_user_by_id(user_id=1, data=data)
#
#     async_mock_session.execute.assert_called_once()
#     async_mock_session.commit.assert_called_once()


@pytest.mark.anyio
async def test_create_user(user_repo, async_mock_session, fake_user):
    schema = UserCreateSchema(
        username=fake_user.username,
        email=fake_user.email,
        password="plaintext"
    )

    async_mock_session.refresh = AsyncMock()

    user = await user_repo.create(user_data=schema.dict(exclude='password'), hashed_password=schema.password)

    async_mock_session.add.assert_called_once()
    async_mock_session.commit.assert_called_once()
    async_mock_session.refresh.assert_called_once_with(user)

    assert isinstance(user, User)
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.hashed_password == "plaintext"
