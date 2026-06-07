import uuid
from datetime import datetime
from pydantic import BaseModel


class PostCreate(BaseModel):
    content: str
    type: str = "general"
    trade_id: str | None = None
    images: list[str] | None = None


class PostUpdate(BaseModel):
    content: str | None = None


class PostResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    content: str
    images: list | None = None
    trade_id: uuid.UUID | None = None
    type: str
    likes_count: int = 0
    comments_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PostWithUserResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    display_name: str
    avatar_url: str | None = None
    content: str
    images: list | None = None
    trade_id: uuid.UUID | None = None
    type: str
    likes_count: int
    comments_count: int
    liked_by_me: bool = False
    created_at: datetime


class CommentCreate(BaseModel):
    content: str
    parent_id: str | None = None


class CommentResponse(BaseModel):
    id: uuid.UUID
    post_id: uuid.UUID
    user_id: uuid.UUID
    parent_id: uuid.UUID | None = None
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class CommentWithUserResponse(BaseModel):
    id: uuid.UUID
    post_id: uuid.UUID
    user_id: uuid.UUID
    display_name: str
    avatar_url: str | None = None
    parent_id: uuid.UUID | None = None
    content: str
    created_at: datetime


class ChatRoomResponse(BaseModel):
    id: uuid.UUID
    name: str
    type: str
    instrument_id: uuid.UUID | None = None
    is_private: bool = False
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatMessageResponse(BaseModel):
    id: uuid.UUID
    room_id: uuid.UUID
    user_id: uuid.UUID
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}
