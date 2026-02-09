import os
import time
import sys
import json
from typing import List
from pt_config import ConfigManager

# Python 3.13 Universal SDK Integration
try:
    from kucoin_universal_sdk.model.client_option import ClientOptionBuilder
    from kucoin_universal_sdk.control.default_client import DefaultClient
    from kucoin_universal_sdk.generate.spot.market.model_get_klines_req import GetKlinesReq
    KUCOIN_AVAILABLE = True
except ImportError:
    KUCOIN_AVAILABLE = False

if KUCOIN_AVAILABLE:
    options = ClientOptionBuilder().build()
    kucoin_client = DefaultClient(options)
    market_api = kucoin_client.rest_service().get_spot_service().get_market_api()
else:
    market_api = None

def get_kucoin_klines(symbol: str, tf: str) -> List[list]:
    """Fetches klines and maps to legacy format."""
    if not market_api: return []
    try:
        req = GetKlinesReq(symbol=symbol, type=tf)
        resp = market_api.get_klines(req)
        return [list(map(str, candle)) for candle in resp.data] if resp and resp.data else []
    except Exception:
        return []

def get_base_dir() -> str:
    """Retrieves the base directory from config or fallback to local path."""
    try:
        cm = ConfigManager()
        # FIX: Use dictionary access for 'trading'
        config_dir = cm.get().trading.get("main_neural_dir")
        if config_dir and os.path.isdir(config_dir):
            return config_dir
    except Exception:
        pass
    return os.path.dirname(os.path.abspath(__file__))

def coin_folder(sym: str) -> str:
    """Revised: ALL coins (including BTC) use their own subdirectory."""
    return os.path.join(get_base_dir(), sym.upper())

def init_coin(sym: str):
    """Initializes subdirectory and signals readiness gate for the Hub."""
    folder = coin_folder(sym)
    os.makedirs(folder, exist_ok=True)
    
    # Readiness Gate for Hub/Trader launch synchronization
    ready_path = os.path.join(folder, "runner_ready.json")
    with open(ready_path, "w") as f:
        json.dump({"ready": True, "ts": time.time()}, f)

if __name__ == "__main__":
    try:
        cm = ConfigManager()
        # FIX: Access 'trading' as a dict to prevent AttributeError
        trading_cfg = cm.get().trading
        
        if not isinstance(trading_cfg, dict):
            print("[pt_thinker] Error: Trading configuration is not a dictionary.")
            sys.exit(1)

        coins = trading_cfg.get("coins", ["BTC"])
        
        for sym in coins:
            init_coin(sym)
            
        print(f"[pt_thinker] Neural engine initialized. Subdirectories verified for: {coins}")
        
        # Keep process alive for the Hub to detect active state
        while True:
            time.sleep(60)
            
    except Exception as e:
        print(f"[pt_thinker] Critical failure during startup: {e}")
        sys.exit(1)