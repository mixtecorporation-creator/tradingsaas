import uuid
from sqlalchemy import String, Text, Integer, ForeignKey, Uuid, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin


class Post(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "posts"

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    images: Mapped[list | None] = mapped_column(JSON, nullable=True)
    trade_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("trades.id"), nullable=True)
    type: Mapped[str] = mapped_column(String(20), nullable=False, default="general")
    likes_count: Mapped[int] = mapped_column(Integer, default=0)
    comments_count: Mapped[int] = mapped_column(Integer, default=0)


class Comment(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "comments"

    post_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("posts.id"), nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("comments.id"), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)


class PostLike(Base):
    __tablename__ = "post_likes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("posts.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False)
