import uuid
from datetime import datetime
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.instrument import Instrument, MarketDataOHLCV


class InstrumentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_active(self) -> list[Instrument]:
        result = await self.db.execute(
            select(Instrument).where(Instrument.active == True).order_by(Instrument.symbol)
        )
        return list(result.scalars().all())

    async def find_by_id(self, id: uuid.UUID) -> Instrument | None:
        result = await self.db.execute(select(Instrument).where(Instrument.id == id))
        return result.scalar_one_or_none()

    async def find_by_symbol(self, symbol: str) -> Instrument | None:
        result = await self.db.execute(
            select(Instrument).where(Instrument.symbol == symbol.upper())
        )
        return result.scalar_one_or_none()

    async def get_ohlcv(
        self, instrument_id: uuid.UUID, timeframe: str, limit: int = 100,
        start: datetime | None = None, end: datetime | None = None,
    ) -> list[MarketDataOHLCV]:
        query = select(MarketDataOHLCV).where(
            MarketDataOHLCV.instrument_id == instrument_id,
            MarketDataOHLCV.timeframe == timeframe,
        )
        if start:
            query = query.where(MarketDataOHLCV.open_time >= start)
        if end:
            query = query.where(MarketDataOHLCV.open_time <= end)
        query = query.order_by(MarketDataOHLCV.open_time.desc()).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
