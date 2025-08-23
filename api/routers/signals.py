# api/routers/signals.py - returns engine signals (uses core.signal_engine)
from fastapi import APIRouter
from ...core.data import load
from ...core.signal_engine import generate_signal
from ...core.config import EngineConfig
from ...core.risk import Risk

router = APIRouter()

@router.get('/signal')
def signal(symbol: str='EURUSD', timeframe: str='15m', bars: int=500, balance: float = 100.0):
    df = load(symbol, timeframe, bars=bars)
    res = generate_signal(df, EngineConfig(), Risk(balance=balance))
    return res
