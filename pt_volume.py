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

# Updated Imports for Python 3.13 and Universal SDK compatibility
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
    total_volume: