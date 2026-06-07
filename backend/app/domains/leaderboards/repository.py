import uuid
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.leaderboard import LeaderboardEntry, Follow, ReputationScore
from app.models.profile import TraderProfile
from app.models.user import User


class LeaderboardRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_entries(self, period: str, limit: int, offset: int) -> list[LeaderboardEntry]:
        result = await self.db.execute(
            select(LeaderboardEntry)
            .where(LeaderboardEntry.period == period)
            .order_by(LeaderboardEntry.rank)
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_reputation(self, user_id: uuid.UUID) -> ReputationScore | None:
        result = await self.db.execute(
            select(ReputationScore).where(ReputationScore.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def is_following(self, follower_id: uuid.UUID, following_id: uuid.UUID) -> bool:
        result = await self.db.execute(
            select(Follow).where(
                Follow.follower_id == follower_id,
                Follow.following_id == following_id,
            )
        )
        return result.scalar_one_or_none() is not None

    async def follow(self, follower_id: uuid.UUID, following_id: uuid.UUID) -> Follow:
        follow = Follow(follower_id=follower_id, following_id=following_id)
        self.db.add(follow)
        await self.db.flush()

        await self.db.execute(
            select(func.count(Follow.id)).where(Follow.following_id == following_id)
        )
        await self.db.execute(
            select(TraderProfile).where(TraderProfile.user_id == following_id)
        )
        return follow

    async def unfollow(self, follower_id: uuid.UUID, following_id: uuid.UUID) -> None:
        await self.db.execute(
            delete(Follow).where(
                Follow.follower_id == follower_id,
                Follow.following_id == following_id,
            )
        )
        await self.db.flush()

    async def get_followers(self, user_id: uuid.UUID) -> list[Follow]:
        result = await self.db.execute(
            select(Follow).where(Follow.following_id == user_id).order_by(Follow.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_following(self, user_id: uuid.UUID) -> list[Follow]:
        result = await self.db.execute(
            select(Follow).where(Follow.follower_id == user_id).order_by(Follow.created_at.desc())
        )
        return list(result.scalars().all())

    async def count_followers(self, user_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(func.count(Follow.id)).where(Follow.following_id == user_id)
        )
        return result.scalar() or 0

    async def count_following(self, user_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(func.count(Follow.id)).where(Follow.follower_id == user_id)
        )
        return result.scalar() or 0
