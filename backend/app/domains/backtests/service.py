import uuid
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.backtests.repository import BacktestRepository
from app.domains.backtests.engine import BacktestEngine
from app.exceptions import NotFoundException


class BacktestService:
    def __init__(self, db: AsyncSession):
        self.repo = BacktestRepository(db)
        self.engine = BacktestEngine(db)

    async def list_runs(self, user_id: uuid.UUID, limit: int = 20, offset: int = 0):
        return await self.repo.list_by_user(user_id, limit, offset)

    async def get_run(self, run_id: str, user_id: uuid.UUID):
        run = await self.repo.find_by_id(uuid.UUID(run_id), user_id)
        if not run:
            raise NotFoundException("Backtest run not found")
        return run

    async def create_and_run(self, user_id: uuid.UUID, data):
        instrument = await self.repo.find_instrument_by_symbol(data.instrument_symbol)
        if not instrument:
            raise NotFoundException(f"Instrument '{data.instrument_symbol}' not found")

        run_data = {
            "instrument_id": instrument.id,
            "strategy_name": data.strategy_name,
            "strategy_config": data.strategy_config,
            "timeframe": data.timeframe,
            "start_date": data.start_date,
            "end_date": data.end_date,
            "initial_capital": Decimal(str(data.initial_capital)),
            "status": "running",
            "started_at": datetime.now(timezone.utc),
        }
        run = await self.repo.create(user_id, run_data)

        try:
            engine_result = await self.engine.run(
                run.id, instrument.id, data.strategy_name, data.strategy_config,
                data.start_date, data.end_date, run.initial_capital,
            )

            if "error" in engine_result:
                run.status = "failed"
                run.error_message = engine_result["error"]
                run.completed_at = datetime.now(timezone.utc)
                return run

            trades = engine_result.pop("trades")
            from app.models.backtest import BacktestResult, BacktestTrade
            result = BacktestResult(
                backtest_run_id=run.id,
                **{k: v for k, v in engine_result.items() if k in [
                    "total_return", "total_return_pct", "max_drawdown", "max_drawdown_pct",
                    "sharpe_ratio", "win_rate", "total_trades", "winning_trades", "losing_trades",
                    "profit_factor", "avg_win", "avg_loss",
                ]},
                summary_json=engine_result,
            )
            for t in trades:
                bt = BacktestTrade(backtest_run_id=run.id, **t)
                self.engine.db.add(bt)

            self.engine.db.add(result)
            run.status = "completed"
            run.completed_at = datetime.now(timezone.utc)
        except Exception as e:
            run.status = "failed"
            run.error_message = str(e)
            run.completed_at = datetime.now(timezone.utc)

        return run

    async def get_result(self, run_id: str, user_id: uuid.UUID):
        run = await self.get_run(run_id, user_id)
        result = await self.repo.get_result(run.id)
        return result

    async def get_trades(self, run_id: str, user_id: uuid.UUID):
        run = await self.get_run(run_id, user_id)
        return await self.repo.get_trades(run.id)

    async def delete_run(self, run_id: str, user_id: uuid.UUID):
        run = await self.get_run(run_id, user_id)
        await self.repo.db.delete(run)
        await self.repo.db.flush()
