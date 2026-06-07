import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.domains.auth.repository import AuthRepository
from app.exceptions import ConflictException, UnauthorizedException
from app.models.user import User


class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = AuthRepository(db)

    async def register(self, email: str, password: str, display_name: str) -> tuple[User, str, str]:
        existing = await self.repo.find_by_email(email)
        if existing:
            raise ConflictException("Email already registered")

        password_hash = hash_password(password)
        user = await self.repo.create(email=email, password_hash=password_hash, display_name=display_name)
        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))
        return user, access_token, refresh_token

    async def login(self, email: str, password: str) -> tuple[User, str, str]:
        user = await self.repo.find_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedException("Invalid email or password")

        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))
        return user, access_token, refresh_token

    async def refresh_access_token(self, refresh_token: str) -> str:
        try:
            payload = decode_token(refresh_token)
            if payload.get("type") != "refresh":
                raise UnauthorizedException("Invalid token type")
            user_id = payload.get("sub")
            if not user_id:
                raise UnauthorizedException("Invalid token payload")
        except ValueError:
            raise UnauthorizedException("Invalid or expired refresh token")

        user = await self.repo.find_by_id(uuid.UUID(user_id))
        if not user:
            raise UnauthorizedException("User not found")

        return create_access_token(subject=str(user.id))

    async def update_user(self, user_id: uuid.UUID, data) -> User:
        user = await self.repo.find_by_id(user_id)
        if not user:
            raise UnauthorizedException("User not found")

        if data.email and data.email != user.email:
            existing = await self.repo.find_by_email(data.email)
            if existing:
                raise ConflictException("Email already in use")
            user.email = data.email

        if data.display_name:
            user.display_name = data.display_name.strip()

        await self.repo.save(user)
        return user
