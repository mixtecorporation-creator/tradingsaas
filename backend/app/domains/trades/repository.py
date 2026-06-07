import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import select, and_, func, case
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.trade import Trade, TradeTag
from app.models.instrument import Instrument


class TradeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_user(
        self, user_id: uuid.UUID, instrument_id: uuid.UUID | None = None,
        direction: str | None = None, tag: str | None = None,
        start_date: datetime | None = None, end_date: datetime | None = None,
        limit: int = 50, offset: int = 0,
    ) -> tuple[list[Trade], int]:
        query = select(Trade).where(Trade.user_id == user_id)
        count_query = select(func.count(Trade.id)).where(Trade.user_id == user_id)

        if instrument_id:
            query = query.where(Trade.instrument_id == instrument_id)
            count_query = count_query.where(Trade.instrument_id == instrument_id)
        if direction:
            query = query.where(Trade.direction == direction)
            count_query = count_query.where(Trade.direction == direction)
        if tag:
            query = query.where(Trade.tags.any(tag))
            count_query = count_query.where(Trade.tags.any(tag))
        if start_date:
            query = query.where(Trade.entry_date >= start_date)
            count_query = count_query.where(Trade.entry_date >= start_date)
        if end_date:
            query = query.where(Trade.entry_date <= end_date)
            count_query = count_query.where(Trade.entry_date <= end_date)

        query = query.order_by(Trade.entry_date.desc()).offset(offset).limit(limit)
        total = await self.db.scalar(count_query)
        result = await self.db.execute(query)
        return list(result.scalars().all()), total or 0

    async def find_by_id(self, trade_id: uuid.UUID, user_id: uuid.UUID) -> Trade | None:
        result = await self.db.execute(
            select(Trade).where(Trade.id == trade_id, Trade.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: uuid.UUID, data: dict) -> Trade:
        trade = Trade(user_id=user_id, **data)
        self.db.add(trade)
        await self.db.flush()
        return trade

    async def update(self, trade: Trade, data: dict) -> Trade:
        for key, value in data.items():
            if value is not None:
                setattr(trade, key, value)
        self.db.add(trade)
        await self.db.flush()
        return trade

    async def delete(self, trade: Trade) -> None:
        await self.db.delete(trade)
        await self.db.flush()

    async def get_stats(self, user_id: uuid.UUID) -> dict:
        trades = await self.db.execute(
            select(Trade).where(Trade.user_id == user_id, Trade.pnl.isnot(None))
        )
        all_trades = list(trades.scalars().all())
        total = len(all_trades)
        if total == 0:
            return {}

        winning = [t for t in all_trades if t.pnl and t.pnl > 0]
        losing = [t for t in all_trades if t.pnl and t.pnl < 0]

        total_pnl = sum((t.pnl or 0) for t in all_trades)
        win_rate = (len(winning) / total * 100) if total else 0
        avg_win = sum((t.pnl or 0) for t in winning) / len(winning) if winning else 0
        avg_loss = sum((t.pnl or 0) for t in losing) / len(losing) if losing else 0

        total_wins = sum(t.pnl for t in winning)
        total_losses = abs(sum(t.pnl for t in losing))
        profit_factor = total_wins / total_losses if total_losses else 0

        largest_win = max((t.pnl or 0) for t in winning) if winning else 0
        largest_loss = min((t.pnl or 0) for t in losing) if losing else 0

        return {
            "total_trades": total,
            "winning_trades": len(winning),
            "losing_trades": len(losing),
            "total_pnl": float(total_pnl),
            "win_rate": round(win_rate, 2),
            "profit_factor": round(profit_factor, 2),
            "avg_win": float(avg_win),
            "avg_loss": float(avg_loss),
            "largest_win": float(largest_win),
            "largest_loss": float(largest_loss),
        }

    async def find_or_create_instrument(self, symbol: str) -> Instrument:
        symbol = symbol.upper()
        result = await self.db.execute(
            select(Instrument).where(Instrument.symbol == symbol)
        )
        inst = result.scalar_one_or_none()
        if not inst:
            inst = Instrument(symbol=symbol, name=symbol, type="crypto", currency="USD")
            self.db.add(inst)
            await self.db.flush()
        return inst
