import logging
from pt_config import ConfigManager

try:
    from alpaca.trading.client import TradingClient
    _ALPACA_AVAILABLE = True
except Exception:
    TradingClient = None
    _ALPACA_AVAILABLE = False

# Audit logging for CISO review
logging.basicConfig(level=logging.INFO, filename='panic_audit.log', 
                    format='%(asctime)s - %(ALERT)s - %(message)s')

def trigger_panic():
    print("!!! PANIC BUTTON ACTIVATED !!!")
    cm = ConfigManager().get()
    cfg = cm.alpaca
    if not _ALPACA_AVAILABLE:
        print("[Panic] Alpaca SDK not available; panic actions are disabled in this environment.")
        return

    # 1. Initialize Client
    client = TradingClient(
        api_key=cfg.get("api_key"),
        secret_key=cfg.get("api_secret"),
        paper=cm.exchange.get("is_sandbox", True)
    )

    try:
        # 2. Cancel all pending orders first to stop the 'Thinker' logic
        print("[1/2] Cancelling all pending orders...")
        cancel_result = client.cancel_orders()
        logging.info(f"Panic: Cancelled all open orders.")

        # 3. Liquidate all positions (Flattening)
        print("[2/2] Liquidating all open positions...")
        client.close_all_positions(cancel_orders=True)
        
        print("\n[SUCCESS] Account is now flat. All positions closed and orders cancelled.")
        logging.info("Panic: All positions liquidated successfully.")

    except Exception as e:
        error_msg = f"PANIC FAILED: {e}"
        print(f"[CRITICAL ERROR] {error_msg}")
        logging.error(error_msg)

if __name__ == "__main__":
    confirm = input("Type 'CONFIRM' to liquidate all positions: ")
    if confirm == "CONFIRM":
        trigger_panic()
    else:
        print("Panic aborted.")