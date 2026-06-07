import uuid
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class TradeAnalysisResponse(BaseModel):
    risk_reward_ratio: float | None = None
    position_size_suggestion: str | None = None
    market_condition: str | None = None
    key_levels: list[str] = []
    sentiment: str | None = None
    confidence: str | None = None
    notes: list[str] = []


class PerformanceSummaryResponse(BaseModel):
    total_trades: int = 0
    win_rate: float = 0
    profit_factor: float = 0
    sharpe_ratio: float | None = None
    max_drawdown_pct: float | None = None
    avg_hold_time: str | None = None
    best_day: str | None = None
    worst_day: str | None = None
    improvement_tips: list[str] = []


class InsightResponse(BaseModel):
    title: str
    description: str
    type: str
    severity: str = "info"
