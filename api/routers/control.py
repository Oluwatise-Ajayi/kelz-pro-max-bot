# api/routers/control.py - control endpoints for MT5 init, start/stop sessions, killer switch
from fastapi import APIRouter
from pydantic import BaseModel
from ...core.session_manager import SessionManager, SessionConfig
from ...core.executor import Executor, ExecOrder
from ...core.brokers.mt5_live import MT5BrokerLive
import asyncio

router = APIRouter()
session_mgr = SessionManager(SessionConfig())
mt5_broker = MT5BrokerLive()
executor = Executor(broker=mt5_broker, worker_count=2)

class StartReq(BaseModel):
    duration_min: int = 240
    cooldown_min: int = 60

class MT5Config(BaseModel):
    path: str | None = None
    login: int | None = None
    password: str | None = None
    server: str | None = None

@router.post('/mt5/init')
async def mt5_init(cfg: MT5Config):
    mt5_broker.path = cfg.path
    mt5_broker.login = cfg.login
    mt5_broker.password = cfg.password
    mt5_broker.server = cfg.server
    ok = mt5_broker.initialize()
    return {'ok': ok, 'account': mt5_broker.account_info() if ok else None}

@router.post('/start_session')
async def start_session(req: StartReq):
    session_mgr.cfg.session_duration_min = req.duration_min
    session_mgr.cfg.cooldown_min = req.cooldown_min
    session_mgr.start_manual()
    await executor.start()
    return {'ok': True, 'status': session_mgr.status()}

@router.post('/stop_session')
async def stop_session():
    session_mgr.stop_manual()
    await executor.stop()
    return {'ok': True, 'status': session_mgr.status()}

@router.post('/killer_switch')
async def killer_switch(close_all: bool = True):
    session_mgr.stop_manual()
    await executor.stop()
    try:
        res = mt5_broker.close_all()
    except Exception as e:
        res = {'ok': False, 'error': str(e)}
    return {'ok': True, 'broker_close': res}

@router.get('/status')
async def status():
    return {'executor_running': executor.running, 'session': session_mgr.status(), 'mt5_account': mt5_broker.account_info()}
