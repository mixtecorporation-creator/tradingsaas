import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Integer, Numeric, DateTime, ForeignKey, Uuid, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, UUIDMixin


class ReputationScore(UUIDMixin, Base):
    __tablename__ = "reputation_scores"

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), unique=True, nullable=False)
    overall_score: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    pnl_score: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    consistency_score: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    risk_score: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    community_score: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    verification_bonus: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class LeaderboardEntry(UUIDMixin, Base):
    __tablename__ = "leaderboard_entries"
    __table_args__ = (
        UniqueConstraint("user_id", "period", name="uq_leaderboard_entry"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False, index=True)
    period: Mapped[str] = mapped_column(String(20), nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    pnl: Mapped[Decimal] = mapped_column(Numeric(20, 8), default=0)
    returns: Mapped[Decimal | None] = mapped_column(Numeric(10, 4))
    win_rate: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    total_trades: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class Follow(Base):
    __tablename__ = "follows"
    __table_args__ = (
        UniqueConstraint("follower_id", "following_id", name="uq_follow"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    follower_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False, index=True)
    following_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
