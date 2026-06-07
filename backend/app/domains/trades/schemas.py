import uuid
from datetime import datetime
from pydantic import BaseModel, field_validator


class TradeCreate(BaseModel):
    instrument_symbol: str
    direction: str = "long"
    entry_price: float
    exit_price: float | None = None
    quantity: float
    entry_date: datetime
    exit_date: datetime | None = None
    fees: float = 0
    setup: str | None = None
    notes: str | None = None
    tags: list[str] | None = None
    setup_rating: int | None = None
    execution_rating: int | None = None
    emotion_before: str | None = None
    emotion_after: str | None = None
    mistake: str | None = None

    @field_validator("direction")
    @classmethod
    def valid_direction(cls, v: str) -> str:
        if v.lower() not in ("long", "short"):
            raise ValueError("Direction must be 'long' or 'short'")
        return v.lower()

    @field_validator("entry_price", "quantity")
    @classmethod
    def positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Value must be positive")
        return v


class TradeUpdate(BaseModel):
    exit_price: float | None = None
    exit_date: datetime | None = None
    pnl: float | None = None
    pnl_percent: float | None = None
    fees: float | None = None
    setup: str | None = None
    notes: str | None = None
    tags: list[str] | None = None
    setup_rating: int | None = None
    execution_rating: int | None = None
    emotion_before: str | None = None
    emotion_after: str | None = None
    mistake: str | None = None


class TradeResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    instrument_id: uuid.UUID
    direction: str
    entry_price: float
    exit_price: float | None = None
    quantity: float
    entry_date: datetime
    exit_date: datetime | None = None
    pnl: float | None = None
    pnl_percent: float | None = None
    fees: float
    setup: str | None = None
    notes: str | None = None
    tags: list | None = None
    screenshots: list | None = None
    setup_rating: int | None = None
    execution_rating: int | None = None
    emotion_before: str | None = None
    emotion_after: str | None = None
    mistake: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class TradeStatsResponse(BaseModel):
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    total_pnl: float = 0
    win_rate: float = 0
    profit_factor: float = 0
    avg_win: float = 0
    avg_loss: float = 0
    largest_win: float = 0
    largest_loss: float = 0


class TagCreate(BaseModel):
    name: str
    color: str = "#6366f1"


class TagResponse(BaseModel):
    id: uuid.UUID
    name: str
    color: str

    model_config = {"from_attributes": True}
