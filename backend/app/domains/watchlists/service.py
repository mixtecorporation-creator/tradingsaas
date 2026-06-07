import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.watchlists.repository import WatchlistRepository
from app.exceptions import NotFoundException


class WatchlistService:
    def __init__(self, db: AsyncSession):
        self.repo = WatchlistRepository(db)

    async def list_watchlists(self, user_id: uuid.UUID):
        return await self.repo.list_by_user(user_id)

    async def get_watchlist(self, watchlist_id: str, user_id: uuid.UUID):
        wl = await self.repo.find_by_id(uuid.UUID(watchlist_id), user_id)
        if not wl:
            raise NotFoundException("Watchlist not found")
        return wl

    async def create_watchlist(self, user_id: uuid.UUID, data):
        return await self.repo.create(user_id, data.model_dump())

    async def update_watchlist(self, watchlist_id: str, user_id: uuid.UUID, data):
        wl = await self.get_watchlist(watchlist_id, user_id)
        return await self.repo.update(wl, data.model_dump(exclude_none=True))

    async def delete_watchlist(self, watchlist_id: str, user_id: uuid.UUID):
        wl = await self.get_watchlist(watchlist_id, user_id)
        await self.repo.delete(wl)

    async def add_item(self, watchlist_id: str, user_id: uuid.UUID, data):
        await self.get_watchlist(watchlist_id, user_id)
        item_data = data.model_dump()
        return await self.repo.add_item(uuid.UUID(watchlist_id), item_data)

    async def remove_item(self, watchlist_id: str, user_id: uuid.UUID, item_id: str):
        await self.get_watchlist(watchlist_id, user_id)
        await self.repo.remove_item(uuid.UUID(item_id))
