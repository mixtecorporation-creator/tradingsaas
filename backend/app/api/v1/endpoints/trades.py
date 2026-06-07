from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.domains.trades.schemas import (
    TradeCreate, TradeUpdate, TradeResponse, TradeStatsResponse,
)
from app.domains.trades.service import TradeService
from datetime import datetime
from typing import Any

router = APIRouter()


@router.get("")
async def list_trades(
    instrument_id: str | None = Query(None),
    direction: str | None = Query(None),
    tag: str | None = Query(None),
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    limit: int = Query(50, le=100),
    offset: int = Query(0),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TradeService(db)
    trades, total = await service.list_trades(
        user.id, instrument_id, direction, tag, start_date, end_date, limit, offset,
    )
    return {
        "items": [TradeResponse.model_validate(t).model_dump(mode="json") for t in trades],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.post("", response_model=TradeResponse, status_code=201)
async def create_trade(
    body: TradeCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TradeService(db)
    trade = await service.create_trade(user.id, body)
    return TradeResponse.model_validate(trade)


@router.get("/stats", response_model=TradeStatsResponse)
async def trade_stats(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TradeService(db)
    stats = await service.get_stats(user.id)
    return TradeStatsResponse(**stats) if stats else TradeStatsResponse()


@router.get("/{trade_id}", response_model=TradeResponse)
async def get_trade(
    trade_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TradeService(db)
    return TradeResponse.model_validate(await service.get_trade(trade_id, user.id))


@router.put("/{trade_id}", response_model=TradeResponse)
async def update_trade(
    trade_id: str,
    body: TradeUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TradeService(db)
    return TradeResponse.model_validate(await service.update_trade(trade_id, user.id, body))


@router.delete("/{trade_id}")
async def delete_trade(
    trade_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TradeService(db)
    await service.delete_trade(trade_id, user.id)
    return {"message": "Trade deleted"}
