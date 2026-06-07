import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.profile import TraderProfile, PerformanceSnapshot


class ProfileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_user_id(self, user_id: uuid.UUID) -> TraderProfile | None:
        result = await self.db.execute(
            select(TraderProfile).where(TraderProfile.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: uuid.UUID) -> TraderProfile:
        profile = TraderProfile(user_id=user_id)
        self.db.add(profile)
        await self.db.flush()
        return profile

    async def update(self, profile: TraderProfile, data: dict) -> TraderProfile:
        for key, value in data.items():
            if value is not None:
                setattr(profile, key, value)
        self.db.add(profile)
        await self.db.flush()
        return profile

    async def get_snapshots(self, user_id: uuid.UUID, limit: int = 12) -> list[PerformanceSnapshot]:
        result = await self.db.execute(
            select(PerformanceSnapshot)
            .where(PerformanceSnapshot.user_id == user_id)
            .order_by(PerformanceSnapshot.period_start.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
