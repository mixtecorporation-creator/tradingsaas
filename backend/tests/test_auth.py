import pytest
from app.domains.auth.service import AuthService
from app.exceptions import ConflictException, UnauthorizedException


@pytest.mark.asyncio
async def test_register_user(db_session):
    service = AuthService(db_session)
    user, access_token, refresh_token = await service.register(
        email="new@example.com",
        password="securepass123",
        display_name="New User",
    )
    assert user.email == "new@example.com"
    assert user.display_name == "New User"
    assert access_token is not None
    assert refresh_token is not None


@pytest.mark.asyncio
async def test_register_duplicate_email(db_session, test_user):
    service = AuthService(db_session)
    with pytest.raises(ConflictException):
        await service.register(
            email="test@example.com",
            password="password123",
            display_name="Another User",
        )


@pytest.mark.asyncio
async def test_login_valid(db_session, test_user):
    service = AuthService(db_session)
    user, access_token, refresh_token = await service.login(
        email="test@example.com",
        password="password123",
    )
    assert user.id == test_user.id
    assert access_token is not None


@pytest.mark.asyncio
async def test_login_invalid_password(db_session, test_user):
    service = AuthService(db_session)
    with pytest.raises(UnauthorizedException):
        await service.login(email="test@example.com", password="wrongpassword")


@pytest.mark.asyncio
async def test_login_nonexistent_user(db_session):
    service = AuthService(db_session)
    with pytest.raises(UnauthorizedException):
        await service.login(email="nonexistent@example.com", password="password123")
