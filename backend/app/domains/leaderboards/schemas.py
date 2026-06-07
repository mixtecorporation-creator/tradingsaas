import uuid
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class LeaderboardQuery(BaseModel):
    period: str = "monthly"
    limit: int = 50
    offset: int = 0


class LeaderboardEntryResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    period: str
    rank: int
    pnl: Decimal
    returns: Decimal | None = None
    win_rate: Decimal | None = None
    total_trades: int = 0
    updated_at: datetime

    model_config = {"from_attributes": True}


class FollowResponse(BaseModel):
    id: int
    follower_id: uuid.UUID
    following_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class LeaderboardUserResponse(BaseModel):
    user_id: uuid.UUID
    display_name: str
    avatar_url: str | None = None
    rank: int
    pnl: Decimal
    returns: Decimal | None = None
    win_rate: Decimal | None = None
    total_trades: int
    verified: bool = False
    is_following: bool = False

    model_config = {"from_attributes": True}
