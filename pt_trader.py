import logging
from typing import Optional, List
from pt_config import ConfigManager

try:
    from alpaca.trading.client import TradingClient
    from alpaca.trading.requests import (
        MarketOrderRequest,
        LimitOrderRequest,
        TakeProfitRequest,
        StopLossRequest,
    )
    from alpaca.trading.enums import OrderSide, TimeInForce, OrderClass
    _ALPACA_AVAILABLE = True
except Exception:
    # Alpaca not installed; provide minimal stubs so module imports cleanly.
    _ALPACA_AVAILABLE = False

    class TradingClient:
        def __init__(self, *args, **kwargs):
            pass

        def get_account(self):
            raise RuntimeError("Alpaca SDK not available in this environment")

        def submit_order(self, *args, **kwargs):
            raise RuntimeError("Alpaca SDK not available in this environment")

        def close_all_positions(self, *args, **kwargs):
            raise RuntimeError("Alpaca SDK not available in this environment")

    class MarketOrderRequest:
        def __init__(self, *args, **kwargs):
            pass

    class LimitOrderRequest(MarketOrderRequest):
        pass

    class TakeProfitRequest:
        def __init__(self, *args, **kwargs):
            pass

    class StopLossRequest:
        def __init__(self, *args, **kwargs):
            pass

    class OrderSide:
        BUY = "buy"
        SELL = "sell"

    class TimeInForce:
        GTC = "gtc"

    class OrderClass:
        BRACKET = "bracket"

# Configure logging for production auditing
logging.basicConfig(level=logging.INFO, filename='trader_audit.log', 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class PowerTrader:
    def __init__(self):
        self.cm = ConfigManager().get()
        cfg = self.cm.alpaca
        # Production Safety: Default to paper=True unless explicitly set to False
        try:
            self.is_paper = self.cm.exchange.get("is_sandbox", True)
        except Exception:
            self.is_paper = True

        if _ALPACA_AVAILABLE:
            self.client = TradingClient(
                api_key=cfg.get("api_key"),
                secret_key=cfg.get("api_secret"),
                paper=self.is_paper,
            )
            logging.info(f"Trader Initialized: Provider=Alpaca, Mode={'PAPER' if self.is_paper else 'LIVE'}")
        else:
            self.client = TradingClient()
            logging.warning("Alpaca SDK not available — trading functionality disabled in this environment.")

    def format_symbol(self, symbol: str) -> str:
        """Production normalization: Handles crypto pairs and stock tickers."""
        s = symbol.upper().replace("-", "").replace("/", "")
        crypto_list = ["BTC", "ETH", "SOL", "AVAX", "ADA", "LINK", "SHIB"]
        if s in crypto_list:
            return f"{s}/USD"
        return s

    def get_buying_power(self) -> float:
        """Checks actual liquid cash available."""
        try:
            account = self.client.get_account()
            return float(account.buying_power)
        except Exception as e:
            logging.error(f"Failed to fetch account balance: {e}")
            return 0.0

    def place_bracket_order(self, symbol: str, qty: float, take_profit_price: float, stop_loss_price: float):
        """
        Executes a Bracket Order: Parent Market Order + TP Limit + SL Stop.
        This is a production best practice for risk management.
        """
        symbol = self.format_symbol(symbol)
        
        # Define the profit and loss legs
        tp_request = TakeProfitRequest(limit_price=take_profit_price)
        sl_request = StopLossRequest(stop_price=stop_loss_price)

        order_data = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.GTC,
            order_class=OrderClass.BRACKET, # Links all three orders
            take_profit=tp_request,
            stop_loss=sl_request
        )

        try:
            order = self.client.submit_order(order_data=order_data)
            logging.info(f"Bracket Order Submitted: {symbol} Qty:{qty} TP:{take_profit_price} SL:{stop_loss_price}")
            return order
        except Exception as e:
            logging.error(f"Bracket Order Failed: {symbol} - {e}")
            return None

    def close_all_positions(self, cancel_orders: bool = True):
        """Panic button/Session end: Liquidates everything."""
        try:
            self.client.close_all_positions(cancel_orders=cancel_orders)
            logging.warning("ALL POSITIONS CLOSED BY SYSTEM")
        except Exception as e:
            logging.error(f"Panic close failed: {e}")

if __name__ == "__main__":
    trader = PowerTrader()
    print(f"System Check: Buying Power = ${trader.get_buying_power():,.2f}")