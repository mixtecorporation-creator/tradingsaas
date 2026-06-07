from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth, instruments, trades, dashboard,
    watchlists, profiles, backtests, leaderboards,
    community, subscriptions, ai,
)

router = APIRouter(prefix="/api/v1")
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(instruments.router, prefix="/instruments", tags=["instruments"])
router.include_router(trades.router, prefix="/trades", tags=["trades"])
router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
router.include_router(watchlists.router, prefix="/watchlists", tags=["watchlists"])
router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
router.include_router(backtests.router, prefix="/backtests", tags=["backtests"])
router.include_router(leaderboards.router, prefix="/leaderboards", tags=["leaderboards"])
router.include_router(community.router, prefix="/community", tags=["community"])
router.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])
router.include_router(ai.router, prefix="/ai", tags=["ai"])
