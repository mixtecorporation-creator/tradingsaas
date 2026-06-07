import uuid
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.watchlist import Watchlist, WatchlistItem


class WatchlistRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_user(self, user_id: uuid.UUID) -> list[Watchlist]:
        result = await self.db.execute(
            select(Watchlist)
            .where(Watchlist.user_id == user_id)
            .options(selectinload(Watchlist.items))
            .order_by(Watchlist.created_at.desc())
        )
        return list(result.scalars().all())

    async def find_by_id(self, watchlist_id: uuid.UUID, user_id: uuid.UUID) -> Watchlist | None:
        result = await self.db.execute(
            select(Watchlist)
            .where(Watchlist.id == watchlist_id, Watchlist.user_id == user_id)
            .options(selectinload(Watchlist.items))
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: uuid.UUID, data: dict) -> Watchlist:
        wl = Watchlist(user_id=user_id, **data)
        self.db.add(wl)
        await self.db.flush()
        return wl

    async def update(self, watchlist: Watchlist, data: dict) -> Watchlist:
        for key, value in data.items():
            if value is not None:
                setattr(watchlist, key, value)
        self.db.add(watchlist)
        await self.db.flush()
        return watchlist

    async def delete(self, watchlist: Watchlist) -> None:
        await self.db.delete(watchlist)
        await self.db.flush()

    async def add_item(self, watchlist_id: uuid.UUID, data: dict) -> WatchlistItem:
        item = WatchlistItem(watchlist_id=watchlist_id, **data)
        self.db.add(item)
        await self.db.flush()
        return item

    async def remove_item(self, item_id: uuid.UUID) -> None:
        result = await self.db.execute(select(WatchlistItem).where(WatchlistItem.id == item_id))
        item = result.scalar_one_or_none()
        if item:
            await self.db.delete(item)
            await self.db.flush()

    async def update_item(self, item: WatchlistItem, data: dict) -> WatchlistItem:
        for key, value in data.items():
            if value is not None:
                setattr(item, key, value)
        self.db.add(item)
        await self.db.flush()
        return item
