import uuid
from datetime import datetime
from pydantic import BaseModel


class InstrumentResponse(BaseModel):
    id: uuid.UUID
    symbol: str
    name: str | None
    type: str
    exchange: str | None
    currency: str
    active: bool

    model_config = {"from_attributes": True}


class OHLCVResponse(BaseModel):
    open_time: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

    model_config = {"from_attributes": True}


class OHLCVParams(BaseModel):
    timeframe: str = "1d"
    limit: int = 100
    start: datetime | None = None
    end: datetime | None = None
