import uuid
from sqlalchemy import String, Text, Integer, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin, UUIDMixin


class Watchlist(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "watchlists"

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    items: Mapped[list["WatchlistItem"]] = relationship(
        "WatchlistItem", back_populates="watchlist",
        cascade="all, delete-orphan", order_by="WatchlistItem.sort_order",
    )


class WatchlistItem(UUIDMixin, Base):
    __tablename__ = "watchlist_items"

    watchlist_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("watchlists.id"), nullable=False, index=True)
    instrument_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("instruments.id"), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    watchlist: Mapped["Watchlist"] = relationship("Watchlist", back_populates="items")
