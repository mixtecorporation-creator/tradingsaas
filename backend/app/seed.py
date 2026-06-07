"""Seed database with common instruments and sample data."""
import asyncio
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import random
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.models.base import Base
from app.models.instrument import Instrument, MarketDataOHLCV
from app.models.user import User
from app.core.security import hash_password

INSTRUMENTS = [
    {"symbol": "BTC/USD", "name": "Bitcoin", "type": "crypto"},
    {"symbol": "ETH/USD", "name": "Ethereum", "type": "crypto"},
    {"symbol": "SOL/USD", "name": "Solana", "type": "crypto"},
    {"symbol": "AAPL", "name": "Apple Inc.", "type": "stock", "exchange": "NASDAQ"},
    {"symbol": "MSFT", "name": "Microsoft Corp.", "type": "stock", "exchange": "NASDAQ"},
    {"symbol": "GOOGL", "name": "Alphabet Inc.", "type": "stock", "exchange": "NASDAQ"},
    {"symbol": "AMZN", "name": "Amazon.com Inc.", "type": "stock", "exchange": "NASDAQ"},
    {"symbol": "TSLA", "name": "Tesla Inc.", "type": "stock", "exchange": "NASDAQ"},
    {"symbol": "EUR/USD", "name": "Euro / US Dollar", "type": "forex"},
    {"symbol": "GBP/USD", "name": "Pound / US Dollar", "type": "forex"},
]

BASE_PRICES = {
    "BTC/USD": 65000, "ETH/USD": 3400, "SOL/USD": 145,
    "AAPL": 220, "MSFT": 430, "GOOGL": 175, "AMZN": 195, "TSLA": 250,
    "EUR/USD": 1.08, "GBP/USD": 1.26,
}

DATABASE_URL = "sqlite+aiosqlite:///./trading.db"


def random_walk(base: float, steps: int, vol: float = 0.02) -> list[dict]:
    prices = []
    price = base
    for i in range(steps):
        change = price * random.gauss(0, vol)
        price += change
        high = price * (1 + abs(random.gauss(0, vol / 2)))
        low = price * (1 - abs(random.gauss(0, vol / 2)))
        prices.append({
            "open": round(price, 2),
            "high": round(high, 2),
            "low": round(max(low, 0.01), 2),
            "close": round(price, 2),
            "volume": round(random.uniform(100, 10000), 2),
        })
    return prices


async def seed():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as db:
        existing = await db.execute(select(Instrument).limit(1))
        if existing.scalar_one_or_none():
            print("Instruments already seeded, skipping.")
            return

        for inst_data in INSTRUMENTS:
            inst = Instrument(**inst_data, currency="USD", active=True)
            db.add(inst)
            await db.flush()

            base = BASE_PRICES[inst.symbol]
            candles = random_walk(base, 200, 0.025 if inst.type == "crypto" else 0.015)

            for i, candle in enumerate(candles):
                ts = datetime.now(timezone.utc) - timedelta(days=200 - i)
                ohlcv = MarketDataOHLCV(
                    instrument_id=inst.id,
                    timeframe="1d",
                    open_time=ts,
                    open=Decimal(str(candle["open"])),
                    high=Decimal(str(candle["high"])),
                    low=Decimal(str(candle["low"])),
                    close=Decimal(str(candle["close"])),
                    volume=Decimal(str(candle["volume"])),
                )
                db.add(ohlcv)

        demo_user = User(
            email="demo@trading.com",
            password_hash=hash_password("demo1234"),
            display_name="Demo Trader",
            role="user",
        )
        db.add(demo_user)
        await db.commit()
        print(f"Seeded {len(INSTRUMENTS)} instruments with OHLCV data + demo user")

    await engine.dispose()


if __name__ == "__main__":
    random.seed(42)
    asyncio.run(seed())
