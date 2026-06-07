import uuid
from datetime import datetime
from pydantic import BaseModel


class WatchlistCreate(BaseModel):
    name: str
    description: str | None = None


class WatchlistUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class WatchlistItemCreate(BaseModel):
    instrument_symbol: str
    notes: str | None = None


class WatchlistItemUpdate(BaseModel):
    notes: str | None = None
    sort_order: int | None = None


class WatchlistItemResponse(BaseModel):
    id: uuid.UUID
    watchlist_id: uuid.UUID
    instrument_id: uuid.UUID
    notes: str | None = None
    sort_order: int = 0

    model_config = {"from_attributes": True}


class WatchlistResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime
    items: list[WatchlistItemResponse] = []

    model_config = {"from_attributes": True}
