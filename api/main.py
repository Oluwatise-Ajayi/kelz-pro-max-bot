# api/main.py - assemble routers and serve static PWA
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import health, signals, trade, control

app = FastAPI(title="BiG Kelz PRO MAX", version="1.0.0")
app.include_router(health.router, tags=['system'])
app.include_router(signals.router, tags=['signals'])
app.include_router(trade.router, tags=['trade'])
app.include_router(control.router, prefix='/control', tags=['control'])

app.mount('/', StaticFiles(directory='static', html=True), name='static')
