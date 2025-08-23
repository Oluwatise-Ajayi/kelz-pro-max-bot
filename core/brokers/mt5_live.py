# core/brokers/mt5_live.py
import MetaTrader5 as mt5
import time, logging
from dataclasses import dataclass

log = logging.getLogger("bigkelz.mt5")
log.setLevel(logging.INFO)

@dataclass
class MT5BrokerLive:
    path: str | None = None
    login: int | None = None
    password: str | None = None
    server: str | None = None

    def initialize(self):
        kwargs = {}
        if self.path:
            kwargs['path'] = self.path
        ok = mt5.initialize(**kwargs)
        if not ok:
            log.error("MT5 initialize failed: %s", mt5.last_error())
            return False
        if self.login:
            success = mt5.login(self.login, password=self.password, server=self.server) if self.password else mt5.login(self.login)
            if not success:
                log.error("MT5 login failed: %s", mt5.last_error())
                return False
        try:
            ai = mt5.account_info()
            log.info("MT5 initialized. Account: %s", ai._asdict().get("login") if ai else None)
        except Exception:
            pass
        return True

    def shutdown(self):
        try:
            mt5.shutdown()
        except Exception as e:
            log.exception("mt5 shutdown: %s", e)

    def symbol_info_tick(self, symbol):
        return mt5.symbol_info_tick(symbol)

    def symbol_info(self, symbol):
        return mt5.symbol_info(symbol)

    def _normalize_symbol(self, symbol):
        s = mt5.symbol_info(symbol)
        if s is not None:
            return symbol
        s = mt5.symbol_info(symbol.upper())
        if s is not None:
            return symbol.upper()
        # attempt to find matching symbol with suffixes
        for sym in mt5.symbols_get():
            if sym.name.upper().startswith(symbol.upper()):
                return sym.name
        raise ValueError(f"symbol {symbol} not available in market watch")

    def place_market(self, order):
        sym = self._normalize_symbol(order.symbol)
        lot = float(order.size)
        si = mt5.symbol_info(sym)
        if si is None:
            return {"ok": False, "error": f"Symbol {sym} not found"}
        if lot < si.volume_min:
            return {"ok": False, "error": f"Lot {lot} below min {si.volume_min}"}
        step = si.volume_step or 0.01
        try:
            # round to step
            lot = max(si.volume_min, round(round(lot/step)*step, 3))
        except Exception:
            lot = max(si.volume_min, round(lot, 3))
        tp = order.tp
        sl = order.sl
        if order.side.upper() == "BUY":
            price = mt5.symbol_info_tick(sym).ask
            order_type = mt5.ORDER_TYPE_BUY
        else:
            price = mt5.symbol_info_tick(sym).bid
            order_type = mt5.ORDER_TYPE_SELL
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": sym,
            "volume": lot,
            "type": order_type,
            "price": price,
            "deviation": 20,
            "magic": 234000,
            "comment": "BiGKelz-Live",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        if sl:
            request["sl"] = float(sl)
        if tp:
            request["tp"] = float(tp)
        result = mt5.order_send(request)
        if result is None:
            return {"ok": False, "error": "order_send returned None"}
        try:
            retcode = getattr(result, "retcode", None)
            if retcode != mt5.TRADE_RETCODE_DONE:
                return {"ok": False, "error": f"retcode={retcode}", "result": result._asdict() if hasattr(result, "_asdict") else str(result)}
            return {"ok": True, "order": result._asdict() if hasattr(result, "_asdict") else str(result)}
        except Exception as e:
            return {"ok": False, "error": str(e), "raw": str(result)}

    def close_all(self, symbol=None):
        pos = mt5.positions_get(symbol=symbol) if symbol else mt5.positions_get()
        if pos is None:
            return {"ok": True, "closed": 0}
        closed = 0
        for p in pos:
            sym = p.symbol
            volume = p.volume
            pos_type = mt5.ORDER_TYPE_SELL if p.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
            price = mt5.symbol_info_tick(sym).bid if pos_type == mt5.ORDER_TYPE_SELL else mt5.symbol_info_tick(sym).ask
            req = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": sym,
                "volume": volume,
                "type": pos_type,
                "position": p.ticket,
                "price": price,
                "deviation": 20,
                "magic": 234000,
                "comment": "BiGKelz close",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            res = mt5.order_send(req)
            if res and getattr(res, "retcode", None) == mt5.TRADE_RETCODE_DONE:
                closed += 1
        return {"ok": True, "closed": closed}

    def account_info(self):
        ai = mt5.account_info()
        return ai._asdict() if ai else None
