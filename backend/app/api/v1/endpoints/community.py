from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.api.deps import get_current_user, get_optional_user
from app.models.user import User
from app.domains.community.schemas import (
    PostCreate, PostResponse, PostWithUserResponse,
    CommentCreate, CommentWithUserResponse,
    ChatRoomResponse, ChatMessageResponse,
)
from app.domains.community.service import CommunityService
from app.domains.auth.repository import AuthRepository

router = APIRouter()


@router.get("/feed")
async def get_feed(
    limit: int = Query(50, le=100),
    offset: int = Query(0),
    user: User | None = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    service = CommunityService(db)
    posts, total = await service.get_feed(limit, offset)
    auth_repo = AuthRepository(db)
    result = []
    for p in posts:
        trader = await auth_repo.find_by_id(p.user_id)
        liked = False
        if user:
            liked = await service.repo.has_liked(p.id, user.id)
        result.append({
            "id": p.id, "user_id": p.user_id,
            "display_name": trader.display_name if trader else "Unknown",
            "avatar_url": trader.avatar_url if trader else None,
            "content": p.content, "images": p.images,
            "trade_id": p.trade_id, "type": p.type,
            "likes_count": p.likes_count, "comments_count": p.comments_count,
            "liked_by_me": liked, "created_at": p.created_at,
        })
    return {"items": result, "total": total, "limit": limit, "offset": offset}


@router.post("/posts", response_model=PostResponse, status_code=201)
async def create_post(
    body: PostCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CommunityService(db)
    post = await service.create_post(user.id, body)
    return PostResponse.model_validate(post).model_dump(mode="json")


@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = CommunityService(db)
    post = await service.get_post(post_id)
    return PostResponse.model_validate(post).model_dump(mode="json")


@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CommunityService(db)
    await service.delete_post(post_id, user.id)
    return {"message": "Post deleted"}


@router.post("/posts/{post_id}/like")
async def like_post(
    post_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CommunityService(db)
    liked = await service.toggle_like(post_id, user.id)
    return {"liked": liked}


@router.get("/posts/{post_id}/comments", response_model=list[CommentWithUserResponse])
async def get_comments(
    post_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = CommunityService(db)
    comments = await service.get_comments(post_id)
    auth_repo = AuthRepository(db)
    result = []
    for c in comments:
        trader = await auth_repo.find_by_id(c.user_id)
        result.append({
            "id": c.id, "post_id": c.post_id, "user_id": c.user_id,
            "display_name": trader.display_name if trader else "Unknown",
            "avatar_url": trader.avatar_url if trader else None,
            "parent_id": c.parent_id, "content": c.content,
            "created_at": c.created_at,
        })
    return result


@router.post("/posts/{post_id}/comments", response_model=CommentWithUserResponse, status_code=201)
async def add_comment(
    post_id: str,
    body: CommentCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CommunityService(db)
    comment = await service.add_comment(post_id, user.id, body)
    trader = await AuthRepository(db).find_by_id(user.id)
    return {
        "id": comment.id, "post_id": comment.post_id, "user_id": comment.user_id,
        "display_name": trader.display_name if trader else "Unknown",
        "avatar_url": trader.avatar_url if trader else None,
        "parent_id": comment.parent_id, "content": comment.content,
        "created_at": comment.created_at,
    }


@router.get("/chat/rooms", response_model=list[ChatRoomResponse])
async def list_rooms(db: AsyncSession = Depends(get_db)):
    service = CommunityService(db)
    rooms = await service.get_chat_rooms()
    return [ChatRoomResponse.model_validate(r).model_dump(mode="json") for r in rooms]


@router.get("/chat/rooms/{room_id}/messages", response_model=list[ChatMessageResponse])
async def get_chat_history(
    room_id: str,
    limit: int = Query(50, le=200),
    db: AsyncSession = Depends(get_db),
):
    service = CommunityService(db)
    msgs = await service.get_chat_history(room_id, limit)
    return [ChatMessageResponse.model_validate(m).model_dump(mode="json") for m in msgs]
