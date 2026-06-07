import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.instruments.repository import InstrumentRepository
from app.exceptions import NotFoundException


class InstrumentService:
    def __init__(self, db: AsyncSession):
        self.repo = InstrumentRepository(db)

    async def list_instruments(self) -> list:
        return await self.repo.list_active()

    async def get_instrument(self, symbol_or_id: str) -> dict:
        try:
            uid = uuid.UUID(symbol_or_id)
            inst = await self.repo.find_by_id(uid)
        except ValueError:
            inst = await self.repo.find_by_symbol(symbol_or_id)
        if not inst:
            raise NotFoundException("Instrument not found")
        return inst

    async def get_ohlcv(
        self, symbol_or_id: str, timeframe: str = "1d",
        limit: int = 100, start: datetime | None = None, end: datetime | None = None,
    ) -> list:
        try:
            uid = uuid.UUID(symbol_or_id)
            inst = await self.repo.find_by_id(uid)
        except ValueError:
            inst = await self.repo.find_by_symbol(symbol_or_id)
        if not inst:
            raise NotFoundException("Instrument not found")
        return await self.repo.get_ohlcv(inst.id, timeframe, limit, start, end)
