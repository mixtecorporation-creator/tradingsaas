import uuid
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel


class ProfileUpdate(BaseModel):
    bio: str | None = None
    experience_level: str | None = None
    trading_style: list[str] | None = None
    preferred_markets: list[str] | None = None
    website_url: str | None = None
    twitter_handle: str | None = None


class ProfileResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    bio: str | None = None
    experience_level: str | None = None
    trading_style: list | None = None
    preferred_markets: list | None = None
    website_url: str | None = None
    twitter_handle: str | None = None
    verified: bool = False
    verified_at: datetime | None = None
    verification_status: str = "unverified"
    total_followers: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProfilePublicResponse(BaseModel):
    user_id: uuid.UUID
    bio: str | None = None
    experience_level: str | None = None
    trading_style: list | None = None
    preferred_markets: list | None = None
    website_url: str | None = None
    twitter_handle: str | None = None
    verified: bool = False
    verification_status: str = "unverified"
    total_followers: int = 0

    model_config = {"from_attributes": True}


class PerformanceSnapshotResponse(BaseModel):
    id: uuid.UUID
    period: str
    period_start: date
    period_end: date
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    total_pnl: Decimal = Decimal("0")
    total_pnl_pct: Decimal | None = None
    win_rate: Decimal | None = None
    profit_factor: Decimal | None = None
    sharpe_ratio: Decimal | None = None
    max_drawdown_pct: Decimal | None = None

    model_config = {"from_attributes": True}
