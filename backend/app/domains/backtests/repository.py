import uuid
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.backtest import BacktestRun, BacktestResult, BacktestTrade
from app.models.instrument import Instrument


class BacktestRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_user(self, user_id: uuid.UUID, limit: int = 20, offset: int = 0) -> tuple[list[BacktestRun], int]:
        query = select(BacktestRun).where(BacktestRun.user_id == user_id).order_by(BacktestRun.created_at.desc())
        count_q = select(func.count(BacktestRun.id)).where(BacktestRun.user_id == user_id)
        total = await self.db.scalar(count_q)
        result = await self.db.execute(query.offset(offset).limit(limit))
        return list(result.scalars().all()), total or 0

    async def find_by_id(self, run_id: uuid.UUID, user_id: uuid.UUID) -> BacktestRun | None:
        result = await self.db.execute(
            select(BacktestRun).where(BacktestRun.id == run_id, BacktestRun.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: uuid.UUID, data: dict) -> BacktestRun:
        run = BacktestRun(user_id=user_id, **data)
        self.db.add(run)
        await self.db.flush()
        return run

    async def get_result(self, run_id: uuid.UUID) -> BacktestResult | None:
        result = await self.db.execute(
            select(BacktestResult).where(BacktestResult.backtest_run_id == run_id)
        )
        return result.scalar_one_or_none()

    async def get_trades(self, run_id: uuid.UUID) -> list[BacktestTrade]:
        result = await self.db.execute(
            select(BacktestTrade)
            .where(BacktestTrade.backtest_run_id == run_id)
            .order_by(BacktestTrade.entry_time)
        )
        return list(result.scalars().all())

    async def find_instrument_by_symbol(self, symbol: str) -> Instrument | None:
        result = await self.db.execute(
            select(Instrument).where(Instrument.symbol == symbol.upper())
        )
        return result.scalar_one_or_none()
