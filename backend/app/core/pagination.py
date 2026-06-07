from pydantic import BaseModel
from typing import Generic, TypeVar, Sequence

T = TypeVar("T")


class PageParams(BaseModel):
    limit: int = 20
    offset: int = 0

    model_config = {"extra": "forbid"}


class CursorParams(BaseModel):
    cursor: str | None = None
    limit: int = 20

    model_config = {"extra": "forbid"}


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    limit: int
    offset: int


class CursorPage(BaseModel, Generic[T]):
    items: list[T]
    next_cursor: str | None
    has_more: bool
