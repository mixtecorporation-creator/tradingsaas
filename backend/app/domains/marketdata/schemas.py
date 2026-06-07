from pydantic import BaseModel
from datetime import datetime


class LivePrice(BaseModel):
    symbol: str
    name: str | None
    price: float
    bid: float
    ask: float
    change: float
    change_pct: float
    high_24h: float
    low_24h: float
    volume_24h: float
    timestamp: datetime


class TickData(BaseModel):
    symbol: str
    price: float
    bid: float
    ask: float
    volume: float
    timestamp: datetime


class CandleSnapshot(BaseModel):
    symbol: str
    timeframe: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    timestamp: datetime
