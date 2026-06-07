from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.domains.backtests.schemas import (
    BacktestCreate, BacktestRunResponse, BacktestResultResponse,
    BacktestTradeResponse, BacktestWithResultResponse,
)
from app.domains.backtests.service import BacktestService

router = APIRouter()


@router.get("")
async def list_runs(
    limit: int = Query(20, le=100),
    offset: int = Query(0),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = BacktestService(db)
    runs, total = await service.list_runs(user.id, limit, offset)
    return {
        "items": [BacktestRunResponse.model_validate(r).model_dump(mode="json") for r in runs],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.post("", response_model=BacktestRunResponse, status_code=201)
async def create_backtest(
    body: BacktestCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = BacktestService(db)
    run = await service.create_and_run(user.id, body)
    return BacktestRunResponse.model_validate(run).model_dump(mode="json")


@router.get("/{run_id}", response_model=BacktestRunResponse)
async def get_run(
    run_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = BacktestService(db)
    run = await service.get_run(run_id, user.id)
    return BacktestRunResponse.model_validate(run).model_dump(mode="json")


@router.get("/{run_id}/result", response_model=BacktestResultResponse)
async def get_result(
    run_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = BacktestService(db)
    result = await service.get_result(run_id, user.id)
    return BacktestResultResponse.model_validate(result).model_dump(mode="json")


@router.get("/{run_id}/trades", response_model=list[BacktestTradeResponse])
async def get_trades(
    run_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = BacktestService(db)
    trades = await service.get_trades(run_id, user.id)
    return [BacktestTradeResponse.model_validate(t).model_dump(mode="json") for t in trades]
