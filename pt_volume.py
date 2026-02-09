#!/usr/bin/env python3
"""
PowerTrader AI - Volume Analysis Module
=====================================
Volume-based trade entry confirmation, analysis, and filtering.

Updated for Python 3.13 and kucoin-universal-sdk.
"""

import sqlite3
import json
import argparse
import sys
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple, Any
from pathlib import Path
from contextlib import contextmanager
import math
from collections import deque

# Updated Imports for Python 3.13 compatibility
try:
    from kucoin_universal_sdk.model.client_option import ClientOptionBuilder
    from kucoin_universal_sdk.control.default_client import DefaultClient
    from kucoin_universal_sdk.generate.spot.market.model_get_klines_req import GetKlinesReq
    KUCOIN_AVAILABLE = True
except ImportError:
    KUCOIN_AVAILABLE = False
    print("[pt_volume] kucoin-universal-sdk not installed. Volume data fetching limited.")

try:
    from pt_analytics import TradeJournal
    ANALYTICS_AVAILABLE = True
except ImportError:
    ANALYTICS_AVAILABLE = False
    print("[pt_volume] pt_analytics module not available - volume decision logging disabled.")

DB_PATH = Path("hub_data/volume.db")

@dataclass
class CandleVolumeData:
    """OHLCV candle data with volume metrics."""
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float

    @property
    def datetime(self) -> datetime:
        return datetime.fromtimestamp(self.timestamp)

@dataclass
class VolumeMetrics:
    """Volume metrics for a single candle."""
    timestamp: int
    volume: float
    volume_sma: float = 0.0
    volume_ema: float = 0.0
    vwap: float = 0.0
    volume_ratio: float = 1.0  
    z_score: float = 0.0
    trend: str = "stable"  
    anomaly: bool = False
    anomaly_type: str = ""  

@dataclass
class VolumeProfile:
    """Volume profile over a period."""
    period: str
    avg_volume: float
    median_volume: float
    p25_volume: float
    p50_volume: float
    p75_volume: float
    p90_volume: float
    std_volume: float
    total_volume: float
    candle_count: int

@dataclass
class VolumeDecision:
    """Volume-based trade entry decision."""
    timestamp: datetime
    coin: str
    price: float
    volume: float
    metrics: VolumeMetrics
    decision: str  
    reason: str
    confidence: float  

@dataclass
class VolumeBacktestConfig:
    """Configuration for volume-based backtesting."""
    min_volume_ratio: float = 0.5  
    max_volume_ratio: float = 3.0  
    high_volume_zscore: float = 2.0  
    low_volume_zscore: float = -2.0  
    require_increasing_volume: bool = False  
    vwap_distance_pct: float = 0.5  

class VolumeAnalyzer:
    """Calculates volume metrics on historical candle data."""
    def __init__(self, sma_periods: int = 20, ema_periods: int = 20):
        self.sma_periods = sma_periods
        self.ema_periods = ema_periods
        self.volume_history: deque = deque(maxlen=max(sma_periods, ema_periods) * 2)
        self.price_volume_history: List[Tuple[float, float]] = []

    def calculate_sma(self, values: List[float], period: int) -> float:
        if len(values) < period:
            return sum(values) / len(values) if values else 0.0
        return sum(values[-period:]) / period

    def calculate_ema(self, current: float, prev_ema: Optional[float], period: int) -> float:
        if prev_ema is None:
            return current
        multiplier = 2 / (period + 1)
        return (current * multiplier) + (prev_ema * (1 - multiplier))

    def calculate_vwap(self, prices: List[float], volumes: List[float]) -> float:
        if not prices or not volumes or len(prices) != len(volumes):
            return 0.0
        total_pv = sum(p * v for p, v in zip(prices, volumes))
        total_volume = sum(volumes)
        return total_pv / total_volume if total_volume > 0 else 0.0

    def calculate_z_score(self, value: float, mean: float, std: float) -> float:
        if std == 0:
            return 0.0
        return (value - mean) / std

    def detect_trend(self, volumes: List[float], min_periods: int = 5) -> str:
        if len(volumes) < min_periods:
            return "stable"
        recent = volumes[-min_periods:]
        avg_first_half = sum(recent[: min_periods // 2]) / (min_periods // 2)
        avg_second_half = sum(recent[min_periods // 2 :]) / (min_periods - min_periods // 2)
        change_pct = (((avg_second_half - avg_first_half) / avg_first_half) * 100 if avg_first_half > 0 else 0)
        if change_pct > 10: return "increasing"
        elif change_pct < -10: return "decreasing"
        return "stable"

    def analyze_candle(self, candle: CandleVolumeData, prev_ema: Optional[float] = None) -> VolumeMetrics:
        self.volume_history.append(candle.volume)
        self.price_volume_history.append((candle.close, candle.volume))
        volume_sma = self.calculate_sma(list(self.volume_history), self.sma_periods)
        volume_ema = self.calculate_ema(candle.volume, prev_ema, self.ema_periods)
        vwap_window = min(50, len(self.price_volume_history))
        recent_prices = [p for p, v in self.price_volume_history[-vwap_window:]]
        recent_volumes = [v for p, v in self.price_volume_history[-vwap_window:]]
        vwap = self.calculate_vwap(recent_prices, recent_volumes)
        volume_ratio = (candle.volume / volume_sma) if volume_sma > 0 else 1.0
        volume_list = list(self.volume_history)
        if len(volume_list) >= 10:
            mean_vol = sum(volume_list) / len(volume_list)
            std_vol = math.sqrt(sum((v - mean_vol) ** 2 for v in volume_list) / len(volume_list))
            z_score = self.calculate_z_score(candle.volume, mean_vol, std_vol)
        else:
            z_score = 0.0
        trend = self.detect_trend(volume_list)
        anomaly = False
        anomaly_type = ""
        if z_score > 2.5:
            anomaly = True
            anomaly_type = "high_volume"
        elif z_score < -2.5:
            anomaly = True
            anomaly_type = "low_volume"
        return VolumeMetrics(
            timestamp=candle.timestamp, volume=candle.volume, volume_sma=volume_sma,
            volume_ema=volume_ema, vwap=vwap, volume_ratio=volume_ratio,
            z_score=z_score, trend=trend, anomaly=anomaly, anomaly_type=anomaly_type,
        )

    def calculate_profile(self, candles: List[CandleVolumeData]) -> VolumeProfile:
        if not candles:
            return VolumeProfile("unknown", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0)
        volumes = [c.volume for c in candles]
        volumes_sorted = sorted(volumes)
        count = len(volumes)
        avg = sum(volumes) / count
        median = volumes_sorted[count // 2]
        total = sum(volumes)
        std = math.sqrt(sum((v - avg) ** 2 for v in volumes) / count) if count > 0 else 0.0
        p25 = volumes_sorted[int(count * 0.25)] if count >= 4 else volumes_sorted[0]
        p50 = volumes_sorted[int(count * 0.50)] if count >= 2 else volumes_sorted[0]
        p75 = volumes_sorted[int(count * 0.75)] if count >= 4 else volumes_sorted[-1]
        p90 = volumes_sorted[int(count * 0.90)] if count >= 10 else volumes_sorted[-1]
        period = f"{candles[0].datetime.date()} to {candles[-1].datetime.date()}"
        return VolumeProfile(period, avg, median, p25, p50, p75, p90, std, total, count)

class VolumeFilter:
    """Filters trade entries based on volume confirmation."""
    def __init__(self, config: Optional[VolumeBacktestConfig] = None):
        self.config = config or VolumeBacktestConfig()

    def should_allow_entry(self, metrics: VolumeMetrics, price: float) -> Tuple[bool, str, float]:
        confidence = 1.0
        if metrics.volume_ratio < self.config.min_volume_ratio:
            return False, f"Volume too low: {metrics.volume_ratio:.2f}x average", 0.3
        if metrics.volume_ratio > self.config.max_volume_ratio:
            return False, f"Volume spike anomaly: {metrics.volume_ratio:.2f}x average", 0.2
        if metrics.z_score > self.config.high_volume_zscore:
            return False, f"High volume anomaly: z-score {metrics.z_score:.2f}", 0.4
        if metrics.z_score < self.config.low_volume_zscore:
            return False, f"Low volume anomaly: z-score {metrics.z_score:.2f}", 0.3
        if self.config.require_increasing_volume and metrics.trend != "increasing":
            return False, f"Volume trend not increasing: {metrics.trend}", 0.6
        if metrics.vwap > 0:
            dist = abs((price - metrics.vwap) / metrics.vwap) * 100
            if dist > self.config.vwap_distance_pct:
                return False, f"Price too far from VWAP: {dist:.2f}%", 0.7
            confidence *= 1.2
        return True, f"Volume confirms entry: {metrics.volume_ratio:.2f}x average", min(confidence, 1.0)

    def make_decision(self, candle: CandleVolumeData, metrics: VolumeMetrics, coin: str) -> VolumeDecision:
        allow, reason, confidence = self.should_allow_entry(metrics, candle.close)
        decision = "allow" if allow else "reject"
        return VolumeDecision(datetime.now(), coin, candle.close, candle.volume, metrics, decision, reason, confidence)

class VolumeDecisionLogger:
    """Logs volume-based trading decisions to database."""
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    @contextmanager
    def _get_conn(self):
        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_db(self):
        with self._get_conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS volume_decisions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP NOT NULL,
                    coin TEXT NOT NULL,
                    price REAL NOT NULL,
                    volume REAL NOT NULL,
                    volume_sma REAL,
                    volume_ema REAL,
                    vwap REAL,
                    volume_ratio REAL,
                    z_score REAL,
                    trend TEXT,
                    anomaly INTEGER,
                    anomaly_type TEXT,
                    decision TEXT NOT NULL,
                    reason TEXT,
                    confidence REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_decisions_coin ON volume_decisions(coin)")

    def log_decision(self, decision: VolumeDecision) -> int:
        with self._get_conn() as conn:
            cursor = conn.execute("""
                INSERT INTO volume_decisions (
                    timestamp, coin, price, volume, volume_sma, volume_ema,
                    vwap, volume_ratio, z_score, trend, anomaly,
                    anomaly_type, decision, reason, confidence
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (decision.timestamp, decision.coin, decision.price, decision.volume,
                  decision.metrics.volume_sma, decision.metrics.volume_ema,
                  decision.metrics.vwap, decision.metrics.volume_ratio,
                  decision.metrics.z_score, decision.metrics.trend,
                  1 if decision.metrics.anomaly else 0, decision.metrics.anomaly_type,
                  decision.decision, decision.reason, decision.confidence))
            return cursor.lastrowid

# =============================================================================
# REFACTORED DATA FETCHING (kucoin-universal-sdk)
# =============================================================================

class VolumeDataFetcher:
    """Fetches OHLCV data using the KuCoin Universal SDK factory pattern."""
    def __init__(self):
        if KUCOIN_AVAILABLE:
            options = ClientOptionBuilder().build() 
            self.client = DefaultClient(options)
        else:
            self.client = None

    def fetch_candles(self, coin: str, start_date: datetime, end_date: datetime, timeframe: str = "1hour") -> List[CandleVolumeData]:
        if not KUCOIN_AVAILABLE:
            raise RuntimeError("kucoin-universal-sdk not installed. Cannot fetch volume data.")

        symbol = f"{coin}-USDT"
        all_candles = []
        market_api = self.client.rest_service().get_spot_service().get_market_api()

        req = GetKlinesReq(
            symbol=symbol,
            type=timeframe,
            start_at=int(start_date.timestamp()),
            end_at=int(end_date.timestamp())
        )

        try:
            resp = market_api.get_klines(req)
            if resp and resp.data:
                for c in resp.data:
                    # Indexing matches KuCoin kline strings: [0]ts, [1]open, [2]close, [3]high, [4]low, [5]vol
                    all_candles.append(CandleVolumeData(
                        timestamp=int(c[0]),
                        open=float(c[1]),
                        close=float(c[2]),
                        high=float(c[3]),
                        low=float(c[4]),
                        volume=float(c[5])
                    ))
        except Exception as e:
            print(f"Error fetching volume data: {e}")

        all_candles.sort(key=lambda x: x.timestamp)
        return all_candles

def main():
    parser = argparse.ArgumentParser(description="PowerTrader AI Volume Analysis")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    analyze_parser = subparsers.add_parser("analyze", help="Analyze volume for a coin")
    analyze_parser.add_argument("coin", help="Coin symbol (e.g., BTC, ETH)")
    analyze_parser.add_argument("--days", type=int, default=30)
    analyze_parser.add_argument("--timeframe", default="1hour")
    
    args = parser.parse_args()
    if args.command == "analyze":
        # Simplified CLI execution for brevity
        print(f"Starting analysis for {args.coin}...")

if __name__ == "__main__":
    main()