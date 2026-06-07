import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.leaderboards.repository import LeaderboardRepository
from app.exceptions import NotFoundException, ConflictException


class LeaderboardService:
    def __init__(self, db: AsyncSession):
        self.repo = LeaderboardRepository(db)

    async def get_leaderboard(self, period: str = "monthly", limit: int = 50, offset: int = 0):
        return await self.repo.get_entries(period, limit, offset)

    async def get_reputation(self, user_id: uuid.UUID):
        score = await self.repo.get_reputation(user_id)
        if not score:
            return {
                "overall_score": 0,
                "pnl_score": 0,
                "consistency_score": 0,
                "risk_score": 0,
                "community_score": 0,
                "verification_bonus": 0,
                "rank": None,
            }
        return score

    async def follow_user(self, follower_id: uuid.UUID, following_id: str):
        following_uuid = uuid.UUID(following_id)
        if follower_id == following_uuid:
            raise ConflictException("Cannot follow yourself")

        existing = await self.repo.is_following(follower_id, following_uuid)
        if existing:
            raise ConflictException("Already following this user")

        return await self.repo.follow(follower_id, following_uuid)

    async def unfollow_user(self, follower_id: uuid.UUID, following_id: str):
        following_uuid = uuid.UUID(following_id)
        await self.repo.unfollow(follower_id, following_uuid)

    async def get_followers(self, user_id: uuid.UUID):
        return await self.repo.get_followers(user_id)

    async def get_following(self, user_id: uuid.UUID):
        return await self.repo.get_following(user_id)

    async def is_following(self, follower_id: uuid.UUID, following_id: str) -> bool:
        return await self.repo.is_following(follower_id, uuid.UUID(following_id))
