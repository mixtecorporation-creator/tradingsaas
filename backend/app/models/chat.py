import uuid
from datetime import datetime
from sqlalchemy import String, Text, Boolean, ForeignKey, DateTime, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, UUIDMixin


class ChatRoom(UUIDMixin, Base):
    __tablename__ = "chat_rooms"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False, default="global")
    instrument_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("instruments.id"), nullable=True)
    is_private: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class ChatMessage(UUIDMixin, Base):
    __tablename__ = "chat_messages"

    room_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("chat_rooms.id"), nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
