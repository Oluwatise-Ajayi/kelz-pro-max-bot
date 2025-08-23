# core/executor.py - Executor using asyncio queue and ThreadPoolExecutor for blocking broker calls
import asyncio, logging, time, os
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Dict, Any

log = logging.getLogger("bigkelz.executor")
log.setLevel(logging.INFO)
os.makedirs("logs", exist_ok=True)

@dataclass
class ExecOrder:
    symbol: str
    side: str
    size: float
    price: Optional[float] = None
    sl: Optional[float] = None
    tp: Optional[float] = None
    meta: Dict[str,Any] = None

class Executor:
    def __init__(self, broker=None, worker_count: int = 2):
        self.broker = broker
        self.worker_count = max(1, worker_count)
        self.queue = asyncio.Queue()
        self.workers = []
        self.running = False
        self._tp = ThreadPoolExecutor(max_workers=4)

    async def start(self):
        if self.running:
            return
        self.running = True
        for _ in range(self.worker_count):
            self.workers.append(asyncio.create_task(self._worker_loop()))
        log.info("Executor started with %d workers", self.worker_count)

    async def stop(self):
        self.running = False
        for _ in range(self.worker_count):
            await self.queue.put(None)
        await asyncio.gather(*self.workers, return_exceptions=True)
        self.workers = []
        log.info("Executor stopped")

    async def submit(self, order: ExecOrder):
        await self.queue.put(order)
        log.info("Order queued: %s %s %s", order.side, order.symbol, order.size)

    async def _worker_loop(self):
        while True:
            item = await self.queue.get()
            if item is None:
                break
            try:
                await self._send_order(item)
            except Exception as e:
                log.exception("Error handling order: %s", e)
            finally:
                self.queue.task_done()

    async def _send_order(self, order: ExecOrder):
        loop = asyncio.get_running_loop()
        def _place():
            try:
                if not self.broker:
                    return {"ok": False, "error": "No broker configured"}
                return self.broker.place_market(order)
            except Exception as e:
                return {"ok": False, "error": str(e)}
        res = await loop.run_in_executor(self._tp, _place)
        # audit log
        try:
            with open("logs/executor_audit.log", "a") as fh:
                fh.write(f"{time.time()},{order.symbol},{order.side},{order.size},{res}\n")
        except Exception:
            pass
        if not res.get("ok"):
            log.warning("Order failed: %s", res.get("error"))
        else:
            log.info("Order executed: %s", res.get("order"))
