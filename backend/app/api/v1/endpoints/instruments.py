from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.domains.instruments.schemas import InstrumentResponse, OHLCVResponse, OHLCVParams
from app.domains.instruments.service import InstrumentService
from app.domains.marketdata.service import market_data_service
from app.domains.marketdata.schemas import LivePrice

router = APIRouter()


@router.get("", response_model=list[InstrumentResponse])
async def list_instruments(db: AsyncSession = Depends(get_db)):
    service = InstrumentService(db)
    return await service.list_instruments()


@router.get("/{symbol_or_id}", response_model=InstrumentResponse)
async def get_instrument(symbol_or_id: str, db: AsyncSession = Depends(get_db)):
    service = InstrumentService(db)
    return await service.get_instrument(symbol_or_id)


@router.get("/live", response_model=list[LivePrice])
async def get_live_prices():
    return market_data_service.get_live_prices()


@router.get("/{symbol_or_id}/ohlcv", response_model=list[OHLCVResponse])
async def get_ohlcv(
    symbol_or_id: str,
    params: OHLCVParams = Depends(),
    db: AsyncSession = Depends(get_db),
):
    service = InstrumentService(db)
    return await service.get_ohlcv(
        symbol_or_id, params.timeframe, params.limit, params.start, params.end,
    )
