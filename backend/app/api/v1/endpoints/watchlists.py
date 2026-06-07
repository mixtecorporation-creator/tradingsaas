import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.domains.watchlists.schemas import (
    WatchlistCreate, WatchlistUpdate, WatchlistResponse,
    WatchlistItemCreate, WatchlistItemResponse,
)
from app.domains.watchlists.service import WatchlistService

router = APIRouter()


@router.get("", response_model=list[WatchlistResponse])
async def list_watchlists(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = WatchlistService(db)
    watchlists = await service.list_watchlists(user.id)
    return [WatchlistResponse.model_validate(w).model_dump(mode="json") for w in watchlists]


@router.post("", response_model=WatchlistResponse, status_code=201)
async def create_watchlist(
    body: WatchlistCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = WatchlistService(db)
    wl = await service.create_watchlist(user.id, body)
    return WatchlistResponse.model_validate(wl).model_dump(mode="json")


@router.get("/{watchlist_id}", response_model=WatchlistResponse)
async def get_watchlist(
    watchlist_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = WatchlistService(db)
    wl = await service.get_watchlist(watchlist_id, user.id)
    return WatchlistResponse.model_validate(wl).model_dump(mode="json")


@router.put("/{watchlist_id}", response_model=WatchlistResponse)
async def update_watchlist(
    watchlist_id: str,
    body: WatchlistUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = WatchlistService(db)
    wl = await service.update_watchlist(watchlist_id, user.id, body)
    return WatchlistResponse.model_validate(wl).model_dump(mode="json")


@router.delete("/{watchlist_id}")
async def delete_watchlist(
    watchlist_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = WatchlistService(db)
    await service.delete_watchlist(watchlist_id, user.id)
    return {"message": "Watchlist deleted"}


@router.post("/{watchlist_id}/items", response_model=WatchlistItemResponse, status_code=201)
async def add_item(
    watchlist_id: str,
    body: WatchlistItemCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = WatchlistService(db)
    item = await service.add_item(watchlist_id, user.id, body)
    return WatchlistItemResponse.model_validate(item).model_dump(mode="json")


@router.delete("/{watchlist_id}/items/{item_id}")
async def remove_item(
    watchlist_id: str,
    item_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = WatchlistService(db)
    await service.remove_item(watchlist_id, user.id, item_id)
    return {"message": "Item removed"}
