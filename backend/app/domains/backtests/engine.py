import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.backtests.repository import BacktestRepository
from app.models.instrument import MarketDataOHLCV
from sqlalchemy import select


class BacktestEngine:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def run(self, run_id: uuid.UUID, instrument_id: uuid.UUID, strategy_name: str, config: dict, start: datetime, end: datetime, initial_capital: Decimal) -> dict:
        ohlcv = await self._fetch_ohlcv(instrument_id, start, end)
        if not ohlcv:
            return {"error": "No OHLCV data found for the given period"}

        trades = self._run_strategy(ohlcv, strategy_name, config)
        result = self._compute_results(trades, initial_capital)
        result["trades"] = trades
        return result

    async def _fetch_ohlcv(self, instrument_id: uuid.UUID, start: datetime, end: datetime) -> list:
        result = await self.db.execute(
            select(MarketDataOHLCV)
            .where(
                MarketDataOHLCV.instrument_id == instrument_id,
                MarketDataOHLCV.open_time >= start,
                MarketDataOHLCV.open_time <= end,
            )
            .order_by(MarketDataOHLCV.open_time)
        )
        return list(result.scalars().all())

    def _run_strategy(self, ohlcv: list, strategy: str, config: dict) -> list:
        if strategy == "sma_crossover":
            return self._sma_crossover(ohlcv, config)
        return []

    def _sma_crossover(self, ohlcv: list, config: dict) -> list:
        fast = config.get("fast_period", 10)
        slow = config.get("slow_period", 30)
        prices = [float(c.close) for c in ohlcv]
        times = [c.open_time for c in ohlcv]

        if len(prices) < slow:
            return []

        fast_sma = self._sma(prices, fast)
        slow_sma = self._sma(prices, slow)
        trades = []
        in_position = False
        entry_price = Decimal("0")
        entry_time = None

        for i in range(slow, len(prices)):
            prev_fast = fast_sma[i - 1] if i > 0 else 0
            prev_slow = slow_sma[i - 1] if i > 0 else 0

            if not in_position and prev_fast <= prev_slow and fast_sma[i] > slow_sma[i]:
                in_position = True
                entry_price = Decimal(str(prices[i]))
                entry_time = times[i]
            elif in_position and prev_fast >= prev_slow and fast_sma[i] < slow_sma[i]:
                in_position = False
                exit_price = Decimal(str(prices[i]))
                pnl = (exit_price - entry_price) * 100
                pnl_pct = ((exit_price - entry_price) / entry_price * 100) if entry_price else Decimal("0")
                trades.append({
                    "entry_time": entry_time,
                    "exit_time": times[i],
                    "direction": "long",
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "quantity": Decimal("100"),
                    "pnl": pnl,
                    "pnl_percent": pnl_pct,
                })

        return trades

    def _sma(self, prices: list, period: int) -> list:
        result = []
        for i in range(len(prices)):
            if i < period - 1:
                result.append(0)
            else:
                result.append(sum(prices[i - period + 1 : i + 1]) / period)
        return result

    def _compute_results(self, trades: list, initial_capital: Decimal) -> dict:
        if not trades:
            return {
                "total_return": Decimal("0"),
                "total_return_pct": Decimal("0"),
                "max_drawdown": Decimal("0"),
                "max_drawdown_pct": Decimal("0"),
                "sharpe_ratio": Decimal("0"),
                "win_rate": Decimal("0"),
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "profit_factor": Decimal("0"),
                "avg_win": Decimal("0"),
                "avg_loss": Decimal("0"),
            }

        total_pnl = sum(t["pnl"] for t in trades)
        total_return_pct = (total_pnl / initial_capital * 100) if initial_capital else Decimal("0")

        winning = [t for t in trades if t["pnl"] > 0]
        losing = [t for t in trades if t["pnl"] < 0]
        total = len(trades)
        win_rate = Decimal(str(len(winning) / total * 100)) if total else Decimal("0")

        total_wins = sum(t["pnl"] for t in winning)
        total_losses = abs(sum(t["pnl"] for t in losing))
        profit_factor = (total_wins / total_losses) if total_losses else Decimal("0")
        avg_win = (total_wins / len(winning)) if winning else Decimal("0")
        avg_loss = (total_losses / len(losing)) if losing else Decimal("0")

        returns = [float(t["pnl_percent"]) for t in trades]
        avg_return = sum(returns) / len(returns) if returns else 0
        variance = sum((r - avg_return) ** 2 for r in returns) / len(returns) if returns else 0
        sharpe = (avg_return / (variance ** 0.5)) if variance > 0 else 0

        peak = initial_capital
        max_dd = Decimal("0")
        max_dd_pct = Decimal("0")
        running = initial_capital
        for t in trades:
            running += t["pnl"]
            if running > peak:
                peak = running
            dd = peak - running
            dd_pct = (dd / peak * 100) if peak else Decimal("0")
            if dd > max_dd:
                max_dd = dd
                max_dd_pct = dd_pct

        return {
            "total_return": total_pnl,
            "total_return_pct": Decimal(str(round(total_return_pct, 4))),
            "max_drawdown": max_dd,
            "max_drawdown_pct": Decimal(str(round(float(max_dd_pct), 4))),
            "sharpe_ratio": Decimal(str(round(sharpe, 4))),
            "win_rate": Decimal(str(round(float(win_rate), 2))),
            "total_trades": total,
            "winning_trades": len(winning),
            "losing_trades": len(losing),
            "profit_factor": Decimal(str(round(float(profit_factor), 4))),
            "avg_win": avg_win,
            "avg_loss": avg_loss,
        }
