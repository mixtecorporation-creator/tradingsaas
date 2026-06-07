import uuid
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.post import Post, Comment, PostLike
from app.models.chat import ChatRoom, ChatMessage


class CommunityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_posts(self, limit: int = 50, offset: int = 0) -> tuple[list[Post], int]:
        count_q = select(func.count(Post.id))
        total = await self.db.scalar(count_q)
        result = await self.db.execute(
            select(Post).order_by(Post.created_at.desc()).offset(offset).limit(limit)
        )
        return list(result.scalars().all()), total or 0

    async def find_post(self, post_id: uuid.UUID) -> Post | None:
        result = await self.db.execute(select(Post).where(Post.id == post_id))
        return result.scalar_one_or_none()

    async def create_post(self, user_id: uuid.UUID, data: dict) -> Post:
        post = Post(user_id=user_id, **data)
        self.db.add(post)
        await self.db.flush()
        return post

    async def update_post(self, post: Post, data: dict) -> Post:
        for k, v in data.items():
            if v is not None:
                setattr(post, k, v)
        self.db.add(post)
        await self.db.flush()
        return post

    async def delete_post(self, post: Post) -> None:
        await self.db.delete(post)
        await self.db.flush()

    async def has_liked(self, post_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        result = await self.db.execute(
            select(PostLike).where(PostLike.post_id == post_id, PostLike.user_id == user_id)
        )
        return result.scalar_one_or_none() is not None

    async def like_post(self, post_id: uuid.UUID, user_id: uuid.UUID) -> None:
        like = PostLike(post_id=post_id, user_id=user_id)
        self.db.add(like)
        await self.db.flush()
        await self.db.execute(
            select(Post).where(Post.id == post_id)
        )

    async def unlike_post(self, post_id: uuid.UUID, user_id: uuid.UUID) -> None:
        await self.db.execute(
            delete(PostLike).where(PostLike.post_id == post_id, PostLike.user_id == user_id)
        )
        await self.db.flush()

    async def get_comments(self, post_id: uuid.UUID) -> list[Comment]:
        result = await self.db.execute(
            select(Comment).where(Comment.post_id == post_id).order_by(Comment.created_at)
        )
        return list(result.scalars().all())

    async def create_comment(self, post_id: uuid.UUID, user_id: uuid.UUID, data: dict) -> Comment:
        comment = Comment(post_id=post_id, user_id=user_id, **data)
        self.db.add(comment)
        await self.db.flush()
        return comment

    async def delete_comment(self, comment_id: uuid.UUID) -> None:
        result = await self.db.execute(select(Comment).where(Comment.id == comment_id))
        c = result.scalar_one_or_none()
        if c:
            await self.db.delete(c)
            await self.db.flush()

    async def list_chat_rooms(self) -> list[ChatRoom]:
        result = await self.db.execute(
            select(ChatRoom).where(ChatRoom.is_private == False).order_by(ChatRoom.created_at)
        )
        return list(result.scalars().all())

    async def get_chat_messages(self, room_id: uuid.UUID, limit: int = 50) -> list[ChatMessage]:
        result = await self.db.execute(
            select(ChatMessage).where(ChatMessage.room_id == room_id)
            .order_by(ChatMessage.created_at.desc()).limit(limit)
        )
        return list(reversed(result.scalars().all()))

    async def save_chat_message(self, room_id: uuid.UUID, user_id: uuid.UUID, content: str) -> ChatMessage:
        msg = ChatMessage(room_id=room_id, user_id=user_id, content=content)
        self.db.add(msg)
        await self.db.flush()
        return msg
