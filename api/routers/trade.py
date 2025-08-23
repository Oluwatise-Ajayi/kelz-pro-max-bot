# api/routers/trade.py - queue trades into executor
from fastapi import APIRouter
from pydantic import BaseModel
from ...core.executor import ExecOrder
from .control import executor

router = APIRouter()

class TradeReq(BaseModel):
    symbol: str
    action: str
    size: float
    sl: float | None = None
    tp: float | None = None

@router.post('/place')
async def place_trade(req: TradeReq):
    order = ExecOrder(symbol=req.symbol, side=req.action, size=req.size, sl=req.sl, tp=req.tp)
    await executor.submit(order)
    return {'ok': True, 'queued': True}
