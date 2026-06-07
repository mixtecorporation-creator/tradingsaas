import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.trades.repository import TradeRepository
from app.exceptions import NotFoundException, ForbiddenException


class TradeService:
    def __init__(self, db: AsyncSession):
        self.repo = TradeRepository(db)

    async def list_trades(
        self, user_id: uuid.UUID, instrument_id: str | None = None,
        direction: str | None = None, tag: str | None = None,
        start_date: datetime | None = None, end_date: datetime | None = None,
        limit: int = 50, offset: int = 0,
    ):
        inst_id = uuid.UUID(instrument_id) if instrument_id else None
        return await self.repo.list_by_user(
            user_id, inst_id, direction, tag, start_date, end_date, limit, offset,
        )

    async def get_trade(self, trade_id: str, user_id: uuid.UUID):
        trade = await self.repo.find_by_id(uuid.UUID(trade_id), user_id)
        if not trade:
            raise NotFoundException("Trade not found")
        return trade

    async def create_trade(self, user_id: uuid.UUID, data):
        instrument = await self.repo.find_or_create_instrument(data.instrument_symbol)
        pnl = None
        pnl_pct = None
        if data.exit_price is not None:
            if data.direction == "long":
                pnl = (data.exit_price - data.entry_price) * data.quantity
            else:
                pnl = (data.entry_price - data.exit_price) * data.quantity
            pnl -= data.fees
            pnl_pct = ((data.exit_price - data.entry_price) / data.entry_price) * 100
            if data.direction == "short":
                pnl_pct = -pnl_pct

        trade_data = {
            "instrument_id": instrument.id,
            "direction": data.direction,
            "entry_price": Decimal(str(data.entry_price)),
            "exit_price": Decimal(str(data.exit_price)) if data.exit_price else None,
            "quantity": Decimal(str(data.quantity)),
            "entry_date": data.entry_date,
            "exit_date": data.exit_date,
            "pnl": Decimal(str(pnl)) if pnl is not None else None,
            "pnl_percent": Decimal(str(pnl_pct)) if pnl_pct is not None else None,
            "fees": Decimal(str(data.fees)),
            "setup": data.setup,
            "notes": data.notes,
            "tags": data.tags,
            "setup_rating": data.setup_rating,
            "execution_rating": data.execution_rating,
            "emotion_before": data.emotion_before,
            "emotion_after": data.emotion_after,
            "mistake": data.mistake,
        }
        return await self.repo.create(user_id, trade_data)

    async def update_trade(self, trade_id: str, user_id: uuid.UUID, data):
        trade = await self.get_trade(trade_id, user_id)
        update_data = data.model_dump(exclude_none=True)
        if "exit_price" in update_data and update_data["exit_price"] is not None:
            exit_p = Decimal(str(update_data["exit_price"]))
            entry_p = trade.entry_price
            qty = trade.quantity
            if trade.direction == "long":
                pnl = (exit_p - entry_p) * qty
            else:
                pnl = (entry_p - exit_p) * qty
            pnl -= (trade.fees or Decimal("0"))
            update_data["pnl"] = pnl
            update_data["pnl_percent"] = ((exit_p - entry_p) / entry_p) * 100
            if trade.direction == "short":
                update_data["pnl_percent"] = -update_data["pnl_percent"]
            update_data["exit_date"] = update_data.get("exit_date") or datetime.utcnow()

        return await self.repo.update(trade, update_data)

    async def delete_trade(self, trade_id: str, user_id: uuid.UUID):
        trade = await self.get_trade(trade_id, user_id)
        await self.repo.delete(trade)

    async def get_stats(self, user_id: uuid.UUID):
        return await self.repo.get_stats(user_id)
