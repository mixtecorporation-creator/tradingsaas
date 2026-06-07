import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.profiles.repository import ProfileRepository
from app.exceptions import NotFoundException


class ProfileService:
    def __init__(self, db: AsyncSession):
        self.repo = ProfileRepository(db)

    async def get_or_create_profile(self, user_id: uuid.UUID) -> tuple:
        profile = await self.repo.find_by_user_id(user_id)
        if not profile:
            profile = await self.repo.create(user_id)
        return profile

    async def get_profile(self, user_id: uuid.UUID):
        profile = await self.repo.find_by_user_id(user_id)
        if not profile:
            raise NotFoundException("Profile not found")
        return profile

    async def update_profile(self, user_id: uuid.UUID, data):
        profile = await self.get_or_create_profile(user_id)
        return await self.repo.update(profile, data.model_dump(exclude_none=True))

    async def get_performance_snapshots(self, user_id: uuid.UUID, limit: int = 12):
        return await self.repo.get_snapshots(user_id, limit)
