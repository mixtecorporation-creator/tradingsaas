import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.api.deps import get_current_user, get_optional_user
from app.models.user import User
from app.domains.profiles.schemas import (
    ProfileUpdate, ProfileResponse, ProfilePublicResponse, PerformanceSnapshotResponse,
)
from app.domains.profiles.service import ProfileService
from app.domains.auth.repository import AuthRepository

router = APIRouter()


@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ProfileService(db)
    profile = await service.get_or_create_profile(user.id)
    return ProfileResponse.model_validate(profile).model_dump(mode="json")


@router.put("/me", response_model=ProfileResponse)
async def update_my_profile(
    body: ProfileUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ProfileService(db)
    profile = await service.update_profile(user.id, body)
    return ProfileResponse.model_validate(profile).model_dump(mode="json")


@router.get("/{user_id}", response_model=ProfilePublicResponse)
async def get_public_profile(
    user_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = ProfileService(db)
    profile = await service.get_profile(uuid.UUID(user_id))
    return ProfilePublicResponse.model_validate(profile).model_dump(mode="json")


@router.get("/{user_id}/performance", response_model=list[PerformanceSnapshotResponse])
async def get_performance(
    user_id: str,
    limit: int = Query(12, le=52),
    db: AsyncSession = Depends(get_db),
):
    service = ProfileService(db)
    snapshots = await service.get_performance_snapshots(uuid.UUID(user_id), limit)
    return [PerformanceSnapshotResponse.model_validate(s).model_dump(mode="json") for s in snapshots]
