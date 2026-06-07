import uuid
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, field_validator


class BacktestCreate(BaseModel):
    instrument_symbol: str
    strategy_name: str
    strategy_config: dict = {}
    timeframe: str = "1d"
    start_date: datetime
    end_date: datetime
    initial_capital: float = 10000

    @field_validator("strategy_name")
    @classmethod
    def valid_strategy(cls, v: str) -> str:
        allowed = ["sma_crossover", "macd", "rsi", "bollinger", "custom"]
        if v not in allowed:
            raise ValueError(f"Strategy must be one of: {', '.join(allowed)}")
        return v


class BacktestRunResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    instrument_id: uuid.UUID
    strategy_name: str
    strategy_config: dict
    timeframe: str
    start_date: datetime
    end_date: datetime
    initial_capital: Decimal
    status: str
    error_message: str | None = None
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None

    model_config = {"from_attributes": True}


class BacktestResultResponse(BaseModel):
    id: uuid.UUID
    backtest_run_id: uuid.UUID
    total_return: Decimal | None = None
    total_return_pct: Decimal | None = None
    max_drawdown: Decimal | None = None
    max_drawdown_pct: Decimal | None = None
    sharpe_ratio: Decimal | None = None
    win_rate: Decimal | None = None
    total_trades: int | None = None
    winning_trades: int | None = None
    losing_trades: int | None = None
    profit_factor: Decimal | None = None
    avg_win: Decimal | None = None
    avg_loss: Decimal | None = None
    summary_json: dict | None = None

    model_config = {"from_attributes": True}


class BacktestTradeResponse(BaseModel):
    id: uuid.UUID
    backtest_run_id: uuid.UUID
    entry_time: datetime
    exit_time: datetime
    direction: str
    entry_price: Decimal
    exit_price: Decimal
    quantity: Decimal
    pnl: Decimal
    pnl_percent: Decimal

    model_config = {"from_attributes": True}


class BacktestWithResultResponse(BaseModel):
    run: BacktestRunResponse
    result: BacktestResultResponse | None = None
    trades: list[BacktestTradeResponse] = []

    model_config = {"from_attributes": True}
