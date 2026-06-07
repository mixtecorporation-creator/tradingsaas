import json
from functools import wraps
from typing import Any, Callable, Optional

from app.redis import get_redis


def cache(ttl: int = 300, key_prefix: str = "cache"):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            r = await get_redis()
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            cached = await r.get(cache_key)
            if cached is not None:
                return json.loads(cached)
            result = await func(*args, **kwargs)
            if result is not None:
                await r.setex(cache_key, ttl, json.dumps(result, default=str))
            return result
        return wrapper
    return decorator


async def invalidate_cache(pattern: str):
    r = await get_redis()
    keys = await r.keys(pattern)
    if keys:
        await r.delete(*keys)
