import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Numeric, Text, DateTime, ForeignKey, JSON, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin


class BacktestRun(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "backtest_runs"

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False, index=True)
    instrument_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("instruments.id"), nullable=False)
    strategy_name: Mapped[str] = mapped_column(String(100), nullable=False)
    strategy_config: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    timeframe: Mapped[str] = mapped_column(String(10), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    initial_capital: Mapped[Decimal] = mapped_column(Numeric(20, 8), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class BacktestResult(UUIDMixin, Base):
    __tablename__ = "backtest_results"

    backtest_run_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("backtest_runs.id"), unique=True, nullable=False
    )
    total_return: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    total_return_pct: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True)
    max_drawdown: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    max_drawdown_pct: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True)
    sharpe_ratio: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True)
    win_rate: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    total_trades: Mapped[int | None] = mapped_column(nullable=True)
    winning_trades: Mapped[int | None] = mapped_column(nullable=True)
    losing_trades: Mapped[int | None] = mapped_column(nullable=True)
    profit_factor: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True)
    avg_win: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    avg_loss: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    summary_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class BacktestTrade(UUIDMixin, Base):
    __tablename__ = "backtest_trades"

    backtest_run_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("backtest_runs.id"), nullable=False, index=True
    )
    entry_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    exit_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    direction: Mapped[str] = mapped_column(String(10), nullable=False)
    entry_price: Mapped[Decimal] = mapped_column(Numeric(20, 8), nullable=False)
    exit_price: Mapped[Decimal] = mapped_column(Numeric(20, 8), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(30, 8), nullable=False)
    pnl: Mapped[Decimal] = mapped_column(Numeric(20, 8), nullable=False)
    pnl_percent: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False)
