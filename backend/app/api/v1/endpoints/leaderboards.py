import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.api.deps import get_current_user, get_optional_user
from app.models.user import User
from app.domains.leaderboards.schemas import (
    LeaderboardEntryResponse, FollowResponse, LeaderboardUserResponse,
)
from app.domains.leaderboards.service import LeaderboardService
from app.domains.auth.repository import AuthRepository
from app.domains.profiles.repository import ProfileRepository

router = APIRouter()


@router.get("")
async def get_leaderboard(
    period: str = Query("monthly", regex="^(weekly|monthly|quarterly|yearly|all_time)$"),
    limit: int = Query(50, le=100),
    offset: int = Query(0),
    user: User | None = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    service = LeaderboardService(db)
    entries = await service.get_leaderboard(period, limit, offset)

    result = []
    auth_repo = AuthRepository(db)
    profile_repo = ProfileRepository(db)

    for entry in entries:
        trader = await auth_repo.find_by_id(entry.user_id)
        profile = await profile_repo.find_by_user_id(entry.user_id)
        is_following = False
        if user:
            is_following = await service.is_following(user.id, str(entry.user_id))

        result.append({
            "user_id": entry.user_id,
            "display_name": trader.display_name if trader else "Unknown",
            "avatar_url": trader.avatar_url if trader else None,
            "rank": entry.rank,
            "pnl": entry.pnl,
            "returns": entry.returns,
            "win_rate": entry.win_rate,
            "total_trades": entry.total_trades,
            "verified": profile.verified if profile else False,
            "is_following": is_following,
        })

    return result


@router.get("/me")
async def my_rank(
    period: str = Query("monthly", regex="^(weekly|monthly|quarterly|yearly|all_time)$"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = LeaderboardService(db)
    entries = await service.get_leaderboard(period, 1000, 0)
    for entry in entries:
        if entry.user_id == user.id:
            return {"rank": entry.rank, "period": period}
    return {"rank": None, "period": period}


@router.post("/follow/{target_user_id}", status_code=201)
async def follow_user(
    target_user_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = LeaderboardService(db)
    follow = await service.follow_user(user.id, target_user_id)
    return {"message": "Now following user"}


@router.delete("/follow/{target_user_id}")
async def unfollow_user(
    target_user_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = LeaderboardService(db)
    await service.unfollow_user(user.id, target_user_id)
    return {"message": "Unfollowed user"}


@router.get("/followers")
async def my_followers(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = LeaderboardService(db)
    followers = await service.get_followers(user.id)
    auth_repo = AuthRepository(db)
    result = []
    for f in followers:
        follower = await auth_repo.find_by_id(f.follower_id)
        result.append({
            "user_id": f.follower_id,
            "display_name": follower.display_name if follower else "Unknown",
            "avatar_url": follower.avatar_url if follower else None,
            "followed_at": f.created_at,
        })
    return result


@router.get("/following")
async def my_following(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = LeaderboardService(db)
    following = await service.get_following(user.id)
    auth_repo = AuthRepository(db)
    result = []
    for f in following:
        followed = await auth_repo.find_by_id(f.following_id)
        result.append({
            "user_id": f.following_id,
            "display_name": followed.display_name if followed else "Unknown",
            "avatar_url": followed.avatar_url if followed else None,
            "followed_at": f.created_at,
        })
    return result
