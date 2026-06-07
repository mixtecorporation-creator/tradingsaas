import uuid
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.trade import Trade
from app.models.instrument import Instrument


class AIService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def analyze_trade(self, trade_id: str, user_id: uuid.UUID) -> dict:
        result = await self.db.execute(
            select(Trade).where(Trade.id == uuid.UUID(trade_id), Trade.user_id == user_id)
        )
        trade = result.scalar_one_or_none()
        if not trade or not trade.pnl:
            return {}

        rr_ratio = None
        if trade.exit_price and trade.entry_price:
            diff = abs(float(trade.exit_price) - float(trade.entry_price))
            stop = diff * 0.5
            target = diff * 1.5
            rr_ratio = round(target / stop, 2) if stop else None

        return {
            "risk_reward_ratio": rr_ratio,
            "position_size_suggestion": "1-2% of portfolio per trade" if trade.quantity else None,
            "market_condition": "Analyzing market context...",
            "key_levels": [f"Entry: {trade.entry_price}", f"Exit: {trade.exit_price or 'Open'}"],
            "sentiment": "bullish" if trade.direction == "long" else "bearish",
            "confidence": "high" if trade.pnl and trade.pnl > 0 else "needs review",
            "notes": [
                f"Trade was {'profitable' if trade.pnl and trade.pnl > 0 else 'unprofitable'}",
                f"Direction: {trade.direction}",
                f"PnL: ${float(trade.pnl):.2f}" if trade.pnl else None,
            ],
        }

    async def get_performance_summary(self, user_id: uuid.UUID) -> dict:
        result = await self.db.execute(
            select(Trade).where(Trade.user_id == user_id, Trade.pnl.isnot(None))
        )
        trades = list(result.scalars().all())
        total = len(trades)
        if total == 0:
            return {}

        winning = [t for t in trades if t.pnl and t.pnl > 0]
        losing = [t for t in trades if t.pnl and t.pnl < 0]
        win_rate = round(len(winning) / total * 100, 1) if total else 0
        total_wins = sum(float(t.pnl) for t in winning)
        total_losses = abs(sum(float(t.pnl) for t in losing))
        profit_factor = round(total_wins / total_losses, 2) if total_losses else 0

        returns = [float(t.pnl_percent or 0) for t in trades if t.pnl_percent]
        avg_return = sum(returns) / len(returns) if returns else 0
        variance = sum((r - avg_return) ** 2 for r in returns) / len(returns) if returns else 0
        sharpe = round(avg_return / (variance ** 0.5), 2) if variance > 0 else None

        tips = []
        if win_rate < 40:
            tips.append("Consider tightening your entry criteria")
        if profit_factor < 1.5:
            tips.append("Let winning trades run longer to improve risk/reward")
        if len(losing) > 0 and total_losses / len(losing) > 200:
            tips.append("Consider reducing position size to manage risk")

        return {
            "total_trades": total,
            "win_rate": win_rate,
            "profit_factor": profit_factor,
            "sharpe_ratio": sharpe,
            "max_drawdown_pct": None,
            "avg_hold_time": None,
            "best_day": None,
            "worst_day": None,
            "improvement_tips": tips,
        }

    async def get_insights(self, user_id: uuid.UUID) -> list[dict]:
        insights = []
        result = await self.db.execute(
            select(Trade).where(Trade.user_id == user_id).order_by(Trade.created_at.desc()).limit(100)
        )
        recent = list(result.scalars().all())
        total = len(recent)

        if total > 0:
            losing = [t for t in recent if t.pnl and t.pnl < 0]
            if len(losing) > total * 0.6:
                insights.append({
                    "title": "High Loss Rate",
                    "description": f"{len(losing)} of your last {total} trades were losers. Consider reviewing your strategy.",
                    "type": "warning",
                    "severity": "high",
                })

            no_stop = [t for t in recent if t.mistake and "stop" in t.mistake.lower()]
            if no_stop:
                insights.append({
                    "title": "Missing Stop Losses",
                    "description": f"{len(no_stop)} trades had stop-loss related mistakes.",
                    "type": "risk",
                    "severity": "medium",
                })

        if not insights:
            insights.append({
                "title": "Keep Trading",
                "description": "Log more trades to receive personalized AI insights.",
                "type": "info",
                "severity": "low",
            })

        return insights
