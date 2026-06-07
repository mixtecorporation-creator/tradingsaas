from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, async_session
from app.models.base import Base
from app.redis import close_redis
from app.api.v1.router import router as v1_router
from app.api.websocket.manager import ws_router, manager
from app.domains.marketdata.service import market_data_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await market_data_service.start(async_session, manager)
    yield
    await market_data_service.stop()
    await engine.dispose()
    await close_redis()


app = FastAPI(
    title="Trading SaaS",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)
app.include_router(ws_router)


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
