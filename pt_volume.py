import pandas as pd
import numpy as np
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import List, Optional
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from pt_config import ConfigManager

@dataclass
class Candle:
    timestamp: float
    open: float
    high: float
    low: float
    close: float
    volume: float

class VolumeDataFetcher:
    def __init__(self):
        # 1. Pull Alpaca Keys from ConfigManager
        self.cm = ConfigManager()
        cfg = self.cm.get().alpaca
        
        # Keys are optional for crypto data, but recommended for higher rate limits
        self.api_key = cfg.get("api_key")
        self.secret_key = cfg.get("api_secret")
        
        # Initialize the Alpaca Crypto Client
        self.client = CryptoHistoricalDataClient(self.api_key, self.secret_key)

    def fetch_candles(self, symbol: str, start: datetime, end: datetime, interval: str = "1hour") -> List[Candle]:
        """Fetches historical data via Alpaca-py and maps it to PowerTrader Candles."""
        
        # Alpaca expects 'BTC/USD'. Logic to handle 'BTC', 'BTC-USDT', or 'BTC/USD'
        base_sym = symbol.split('-')[0].split('/')[0].upper()
        formatted_symbol = f"{base_sym}/USD"
        
        # Map PowerTrader intervals to Alpaca TimeFrames
        tf_map = {
            "1min": TimeFrame.Minute,
            "15min": TimeFrame.Minute * 15,
            "1hour": TimeFrame.Hour,
            "1day": TimeFrame.Day
        }
        alpaca_tf = tf_map.get(interval.lower(), TimeFrame.Hour)

        try:
            # Create request object
            request_params = CryptoBarsRequest(
                symbol_or_symbols=[formatted_symbol],
                timeframe=alpaca_tf,
                start=start,
                end=end
            )
            
            # Execute request
            bars = self.client.get_crypto_bars(request_params)
            df = bars.df
            
            if df is None or df.empty:
                print(f"[VolumeFetcher] No data returned for {formatted_symbol}")
                return []

            # bars.df is a MultiIndex (symbol, timestamp). We isolate our symbol.
            symbol_df = df.xs(formatted_symbol)
            
            candles = []
            for ts, row in symbol_df.iterrows():
                candles.append(Candle(
                    timestamp=ts.timestamp(),
                    open=float(row['open']),
                    high=float(row['high']),
                    low=float(row['low']),
                    close=float(row['close']),
                    volume=float(row['volume']) # Alpaca uses 'volume' attribute
                ))
            
            return candles

        except Exception as e:
            print(f"[VolumeFetcher] Alpaca API Error: {e}")
            return []

    def calculate_volume_z_score(self, candles: List[Candle], window: int = 24) -> float:
        """Calculates the current volume anomaly Z-Score based on the recent window."""
        if len(candles) < window:
            return 0.0
            
        volumes = [c.volume for c in candles]
        current_vol = volumes[-1]
        historical_vols = volumes[-window:-1]
        
        mean_vol = np.mean(historical_vols)
        std_vol = np.std(historical_vols)
        
        if std_vol == 0:
            return 0.0
            
        z_score = (current_vol - mean_vol) / std_vol
        return float(z_score)

if __name__ == "__main__":
    # Quick Test
    from datetime import timedelta
    fetcher = VolumeDataFetcher()
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=2)
    
    test_candles = fetcher.fetch_candles("BTC", start_time, end_time)
    if test_candles:
        z = fetcher.calculate_volume_z_score(test_candles)
        print(f"Verified: {len(test_candles)} candles retrieved. Current BTC Volume Z-Score: {z:.2f}")