import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.community.repository import CommunityRepository
from app.domains.auth.repository import AuthRepository
from app.exceptions import NotFoundException, ConflictException


class CommunityService:
    def __init__(self, db: AsyncSession):
        self.repo = CommunityRepository(db)
        self.auth_repo = AuthRepository(db)

    async def get_feed(self, limit: int = 50, offset: int = 0):
        posts, total = await self.repo.list_posts(limit, offset)
        return posts, total

    async def get_post(self, post_id: str):
        post = await self.repo.find_post(uuid.UUID(post_id))
        if not post:
            raise NotFoundException("Post not found")
        return post

    async def create_post(self, user_id: uuid.UUID, data):
        post_data = {"content": data.content, "type": data.type}
        if data.trade_id:
            post_data["trade_id"] = uuid.UUID(data.trade_id)
        if data.images:
            post_data["images"] = data.images
        return await self.repo.create_post(user_id, post_data)

    async def delete_post(self, post_id: str, user_id: uuid.UUID):
        post = await self.get_post(post_id)
        if post.user_id != user_id:
            from app.exceptions import ForbiddenException
            raise ForbiddenException("Not your post")
        await self.repo.delete_post(post)

    async def toggle_like(self, post_id: str, user_id: uuid.UUID) -> bool:
        p_id = uuid.UUID(post_id)
        post = await self.repo.find_post(p_id)
        if not post:
            raise NotFoundException("Post not found")

        liked = await self.repo.has_liked(p_id, user_id)
        if liked:
            await self.repo.unlike_post(p_id, user_id)
            post.likes_count = max(0, post.likes_count - 1)
        else:
            await self.repo.like_post(p_id, user_id)
            post.likes_count += 1
        return not liked

    async def get_comments(self, post_id: str):
        p_id = uuid.UUID(post_id)
        post = await self.repo.find_post(p_id)
        if not post:
            raise NotFoundException("Post not found")
        return await self.repo.get_comments(p_id)

    async def add_comment(self, post_id: str, user_id: uuid.UUID, data):
        p_id = uuid.UUID(post_id)
        post = await self.repo.find_post(p_id)
        if not post:
            raise NotFoundException("Post not found")
        comment_data = {"content": data.content}
        if data.parent_id:
            comment_data["parent_id"] = uuid.UUID(data.parent_id)
        comment = await self.repo.create_comment(p_id, user_id, comment_data)
        post.comments_count += 1
        return comment

    async def get_chat_rooms(self):
        return await self.repo.list_chat_rooms()

    async def get_chat_history(self, room_id: str, limit: int = 50):
        return await self.repo.get_chat_messages(uuid.UUID(room_id), limit)
