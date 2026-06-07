from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.domains.trades.service import TradeService

router = APIRouter()


@router.get("/stats")
async def dashboard_stats(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TradeService(db)
    stats = await service.get_stats(user.id)
    total_trades = stats.get("total_trades", 0) if stats else 0
    return {
        "total_trades": total_trades,
        "total_pnl": stats.get("total_pnl", 0) if stats else 0,
        "win_rate": stats.get("win_rate", 0) if stats else 0,
        "profit_factor": stats.get("profit_factor", 0) if stats else 0,
    }
