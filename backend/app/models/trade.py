import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Numeric, Text, DateTime, Integer, ForeignKey, Uuid, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin


class Trade(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "trades"

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False, index=True)
    instrument_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("instruments.id"), nullable=False)
    direction: Mapped[str] = mapped_column(String(10), nullable=False)
    entry_price: Mapped[Decimal] = mapped_column(Numeric(20, 8), nullable=False)
    exit_price: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(30, 8), nullable=False)
    entry_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    exit_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    pnl: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    pnl_percent: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True)
    fees: Mapped[Decimal] = mapped_column(Numeric(20, 8), default=0)
    setup: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[list | None] = mapped_column(JSON, nullable=True)
    screenshots: Mapped[list | None] = mapped_column(JSON, nullable=True)
    setup_rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    execution_rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    emotion_before: Mapped[str | None] = mapped_column(String(50), nullable=True)
    emotion_after: Mapped[str | None] = mapped_column(String(50), nullable=True)
    mistake: Mapped[str | None] = mapped_column(String(100), nullable=True)


class TradeTag(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "trade_tags"

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    color: Mapped[str] = mapped_column(String(7), nullable=False, default="#6366f1")
