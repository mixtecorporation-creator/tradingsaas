import uuid
from fastapi import Depends, Cookie, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.user import User
from app.core.security import decode_token
from app.exceptions import UnauthorizedException, ForbiddenException


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    authorization: str | None = Header(None),
    access_token: str | None = Cookie(None),
) -> User:
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
    elif access_token:
        token = access_token

    if not token:
        raise UnauthorizedException("Missing authentication token")

    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise UnauthorizedException("Invalid token type")
        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedException("Invalid token payload")
    except ValueError:
        raise UnauthorizedException("Invalid or expired token")

    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    if not user:
        raise UnauthorizedException("User not found")
    return user


async def get_optional_user(
    db: AsyncSession = Depends(get_db),
    authorization: str | None = Header(None),
    access_token: str | None = Cookie(None),
) -> User | None:
    try:
        return await get_current_user(db, authorization, access_token)
    except Exception:
        return None


def require_role(role: str):
    async def role_checker(user: User = Depends(get_current_user)) -> User:
        if user.role != role and user.role != "admin":
            raise ForbiddenException(f"Requires {role} role")
        return user
    return role_checker
