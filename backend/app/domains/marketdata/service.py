import asyncio
import random
import math
from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.domains.marketdata.schemas import LivePrice, TickData, CandleSnapshot
from app.models.instrument import Instrument, MarketDataOHLCV


class MarketDataService:
    def __init__(self):
        self.prices: dict[str, LivePrice] = {}
        self._tick_buffer: dict[str, list[TickData]] = {}
        self._task: asyncio.Task | None = None
        self._manager: object | None = None

    async def prices_from_db(self, db: AsyncSession) -> list[LivePrice]:
        result = await db.execute(
            select(Instrument).where(Instrument.active == True).order_by(Instrument.symbol)
        )
        instruments: list[Instrument] = list(result.scalars().all())

        live_prices: list[LivePrice] = []
        for inst in instruments:
            last_candle = await db.execute(
                select(MarketDataOHLCV)
                .where(
                    MarketDataOHLCV.instrument_id == inst.id,
                    MarketDataOHLCV.timeframe == "1d",
                )
                .order_by(MarketDataOHLCV.open_time.desc())
                .limit(1)
            )
            candle = last_candle.scalar_one_or_none()
            close = candle.close if candle else 100.0
            high_24 = candle.high if candle else close * 1.02
            low_24 = candle.low if candle else close * 0.98
            vol = float(candle.volume) if candle and candle.volume else 1000.0

            now = datetime.now(timezone.UTC)
            live_prices.append(LivePrice(
                symbol=inst.symbol,
                name=inst.name or inst.symbol,
                price=close,
                bid=round(close * 0.9998, 2),
                ask=round(close * 1.0002, 2),
                change=0.0,
                change_pct=0.0,
                high_24h=high_24,
                low_24h=low_24,
                volume_24h=vol,
                timestamp=now,
            ))

        return live_prices

    def _generate_tick(self, price: LivePrice) -> TickData:
        now = datetime.now(timezone.UTC)
        volatility = price.price * 0.0002
        change = random.gauss(0, volatility)
        new_price = max(price.price + change, price.price * 0.9)
        spread = new_price * 0.0004
        bid = round(new_price - spread / 2, 2)
        ask = round(new_price + spread / 2, 2)

        return TickData(
            symbol=price.symbol,
            price=round(new_price, 2),
            bid=bid,
            ask=ask,
            volume=round(random.uniform(0.1, 5.0), 2),
            timestamp=now,
        )

    def _apply_tick(self, tick: TickData):
        prev = self.prices.get(tick.symbol)
        if prev:
            change = tick.price - prev.price
            change_pct = (change / prev.price) * 100 if prev.price else 0.0
            high_24h = max(prev.high_24h, tick.price)
            low_24h = min(prev.low_24h, tick.price)
            volume_24h = prev.volume_24h + tick.volume
            self.prices[tick.symbol] = LivePrice(
                symbol=prev.symbol,
                name=prev.name,
                price=tick.price,
                bid=tick.bid,
                ask=tick.ask,
                change=round(change, 2),
                change_pct=round(change_pct, 2),
                high_24h=high_24h,
                low_24h=low_24h,
                volume_24h=round(volume_24h, 2),
                timestamp=tick.timestamp,
            )

    def get_live_prices(self) -> list[LivePrice]:
        return list(self.prices.values())

    def get_price(self, symbol: str) -> LivePrice | None:
        return self.prices.get(symbol.upper())

    async def start(self, session_factory: async_sessionmaker[AsyncSession], manager: object):
        self._manager = manager
        async with session_factory() as db:
            prices = await self.prices_from_db(db)
            for p in prices:
                self.prices[p.symbol] = p

        self._task = asyncio.create_task(self._tick_loop(session_factory))

    async def stop(self):
        if self._task:
            self._task.cancel()
            self._task = None

    async def _tick_loop(self, session_factory: async_sessionmaker[AsyncSession]):
        while True:
            try:
                await asyncio.sleep(1)
                now = datetime.now(timezone.UTC)
                ticks: list[TickData] = []

                for symbol, price in list(self.prices.items()):
                    tick = self._generate_tick(price)
                    self._apply_tick(tick)
                    ticks.append(tick)

                if self._manager and ticks:
                    for tick in ticks:
                        data = tick.model_dump(mode="json")
                        data["type"] = "tick"
                        await self._manager.broadcast(f"market:{tick.symbol}", data)
                        await self._manager.broadcast("market:all", data)

                        candle_data = {
                            "type": "candle",
                            "symbol": tick.symbol,
                            "timeframe": "1s",
                            "open": self.prices[tick.symbol].price,
                            "high": self.prices[tick.symbol].price,
                            "low": self.prices[tick.symbol].price,
                            "close": tick.price,
                            "volume": tick.volume,
                            "timestamp": now.isoformat(),
                        }
                        await self._manager.broadcast(f"market:{tick.symbol}", candle_data)
                        await self._manager.broadcast("market:all", candle_data)

            except asyncio.CancelledError:
                break
            except Exception:
                pass


market_data_service = MarketDataService()
