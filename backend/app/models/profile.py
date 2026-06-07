import uuid
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import String, Text, Boolean, Integer, Numeric, DateTime, Date, ForeignKey, JSON, Uuid, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin


class TraderProfile(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "trader_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), unique=True, nullable=False)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    experience_level: Mapped[str | None] = mapped_column(String(20), nullable=True)
    trading_style: Mapped[list | None] = mapped_column(JSON, nullable=True)
    preferred_markets: Mapped[list | None] = mapped_column(JSON, nullable=True)
    website_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    twitter_handle: Mapped[str | None] = mapped_column(String(100), nullable=True)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    verification_status: Mapped[str] = mapped_column(String(20), default="unverified")
    total_followers: Mapped[int] = mapped_column(Integer, default=0)


class VerificationDocument(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "verification_documents"

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False)
    document_type: Mapped[str] = mapped_column(String(50), nullable=False)
    document_url: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    reviewed_by: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("users.id"), nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class PerformanceSnapshot(UUIDMixin, Base):
    __tablename__ = "performance_snapshots"
    __table_args__ = (
        UniqueConstraint("user_id", "period", "period_start", name="uq_perf_snapshot"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False, index=True)
    period: Mapped[str] = mapped_column(String(20), nullable=False)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    total_trades: Mapped[int] = mapped_column(Integer, default=0)
    winning_trades: Mapped[int] = mapped_column(Integer, default=0)
    losing_trades: Mapped[int] = mapped_column(Integer, default=0)
    total_pnl: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    total_pnl_pct: Mapped[Decimal | None] = mapped_column(Numeric(10, 4))
    avg_win: Mapped[Decimal | None] = mapped_column(Numeric(20, 8))
    avg_loss: Mapped[Decimal | None] = mapped_column(Numeric(20, 8))
    win_rate: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    profit_factor: Mapped[Decimal | None] = mapped_column(Numeric(10, 4))
    sharpe_ratio: Mapped[Decimal | None] = mapped_column(Numeric(10, 4))
    max_drawdown: Mapped[Decimal | None] = mapped_column(Numeric(20, 8))
    max_drawdown_pct: Mapped[Decimal | None] = mapped_column(Numeric(10, 4))
