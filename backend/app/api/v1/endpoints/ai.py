from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.domains.ai.schemas import TradeAnalysisResponse, PerformanceSummaryResponse, InsightResponse
from app.domains.ai.service import AIService

router = APIRouter()


@router.get("/analyze/trade/{trade_id}", response_model=TradeAnalysisResponse)
async def analyze_trade(
    trade_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AIService(db)
    return await service.analyze_trade(trade_id, user.id)


@router.get("/performance", response_model=PerformanceSummaryResponse)
async def performance_summary(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AIService(db)
    result = await service.get_performance_summary(user.id)
    return PerformanceSummaryResponse(**result) if result else PerformanceSummaryResponse()


@router.get("/insights", response_model=list[InsightResponse])
async def get_insights(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AIService(db)
    return await service.get_insights(user.id)
