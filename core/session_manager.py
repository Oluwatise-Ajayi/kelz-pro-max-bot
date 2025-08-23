# core/session_manager.py - 4hr trading sessions with 1hr cooldown and manual override
import asyncio, logging
from dataclasses import dataclass

log = logging.getLogger("bigkelz.session")
log.setLevel(logging.INFO)

@dataclass
class SessionConfig:
    trading_on: bool = False
    session_duration_min: int = 240  # 4 hours
    cooldown_min: int = 60           # 1 hour
    manual_override: bool = False

class SessionManager:
    def __init__(self, cfg: SessionConfig = None):
        self.cfg = cfg or SessionConfig()
        self._session_task = None
        self._stop_requested = False

    def start_manual(self):
        self.cfg.trading_on = True
        self.cfg.manual_override = True
        if self._session_task is None or self._session_task.done():
            self._session_task = asyncio.create_task(self._session_flow())

    def stop_manual(self):
        self.cfg.trading_on = False
        self.cfg.manual_override = False
        self._stop_requested = True

    async def _session_flow(self):
        while self.cfg.trading_on and not self._stop_requested:
            log.info("Trading session active for %d minutes", self.cfg.session_duration_min)
            await asyncio.sleep(self.cfg.session_duration_min * 60)
            self.cfg.trading_on = False
            log.info("Session ended. Starting cooldown for %d minutes", self.cfg.cooldown_min)
            await asyncio.sleep(self.cfg.cooldown_min * 60)
            if self.cfg.manual_override:
                self.cfg.trading_on = True
                continue
            break

    def status(self):
        return {
            "trading_on": self.cfg.trading_on,
            "manual_override": self.cfg.manual_override,
            "session_duration_min": self.cfg.session_duration_min,
            "cooldown_min": self.cfg.cooldown_min
        }
