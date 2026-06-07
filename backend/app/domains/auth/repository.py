import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def find_by_id(self, user_id: uuid.UUID) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, email: str, password_hash: str, display_name: str) -> User:
        user = User(email=email, password_hash=password_hash, display_name=display_name)
        self.db.add(user)
        await self.db.flush()
        return user

    async def save(self, user: User) -> None:
        self.db.add(user)
        await self.db.flush()
