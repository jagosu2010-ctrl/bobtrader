#!/usr/bin/env python3
"""
PowerTrader AI - Volume Analysis Module
=======================================
Implements volume-based trade entry confirmation and analysis.

Features:
1. Simple Moving Averages (SMA, EMA)
2. Volume-weighted average price (VWAP)
3. Volume anomaly detection (z-score based)
4. Volume trend analysis (increasing/decreasing/stable)
5. CLI tools for volume backtesting

Integrates with pt_thinker.py to add volume data to predictions.
"""

import json
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class VolumeMetrics:
    timestamp: float
    close: float
    volume: float
    sma_10: float
    sma_50: float
    ema_12: float
    vwap: float
    volume_ma_20: float


@dataclass
class VolumeFilter:
    min_volume_avg: float
    min_volume_pct: float = 0.8
    volume_threshold: float = 0.0


class VolumeAnalyzer:
    def __init__(self):
        self.history = []
    
    def calculate_metrics(self, candles: List[Dict]) -> VolumeMetrics:
        volumes = [c["volume"] for c in candles]
        closes = [c["close"] for c in candles]
        prices = [(c["open"] + c["close"]) / 2 for c in candles]
        
        if not volumes or not closes:
            return VolumeMetrics(timestamp=candles[-1]["timestamp"], close=0, volume=0, sma_10=0, sma_50=0, ema_12=0, vwap=0, volume_ma_20=0)
        
        avg_volume = sum(volumes) / len(volumes)
        sma_10 = self._calculate_sma(prices, 10, volumes)
        sma_50 = self._calculate_sma(prices, 50, volumes)
        ema_12 = self._calculate_ema(prices, 12, volumes)
        
        vwap = sum(p * v for p, v in zip(prices, volumes)) / sum(volumes)
        
        return VolumeMetrics(
            timestamp=candles[-1]["timestamp"],
            close=closes[-1],
            volume=avg_volume,
            sma_10=sma_10,
            sma_50=sma_50,
            ema_12=ema_12,
            vwap=vwap,
            volume_ma_20=sum(volumes[-20:]) / 20
        )
    
    def _calculate_sma(self, prices: List[float], period: int, volumes: List[float]) -> float:
        weights = [1/period] * i for i in range(1, period + 1)]
        return sum(p * w for p, w in zip(prices, volumes)) / sum(volumes)
    
    def _calculate_ema(self, prices: List[float], period: int, volumes: List[float]) -> float:
        multiplier = 2 / (period + 1)
        ema = volumes[-1]
        for i in range(1, period):
            alpha = multiplier
            ema = (alpha * prices[i] + (1 - alpha) * ema) / (period + 1)
        return ema
    
    def calculate_trend(self, volumes: List[float]) -> str:
        if len(volumes) < 20:
            return "insufficient"
        
        recent = volumes[-10:]
        early = volumes[-20:-11]
        
        recent_avg = sum(recent) / len(recent)
        early_avg = sum(early) / len(early)
        
        if recent_avg > early_avg * 1.05:
            return "increasing"
        elif recent_avg < early_avg * 0.95:
            return "decreasing"
        else:
            return "stable"
    
    def detect_anomaly(self, current_volume: float, metrics: VolumeMetrics) -> bool:
        if metrics.volume == 0:
            return False
        
        z_score = (current_volume - metrics.sma_10) / metrics.volume_ma_20 if metrics.volume_ma_20 else 1
        return abs(z_score) > 2


class VolumeCLI:
    def analyze_volume(self, symbol: str, start_date: str, end_date: str) -> Dict:
        results = {
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date,
            "metrics": {
                "avg_volume": 0.0,
                "trend": "stable",
                "anomalies_detected": 0
            }
        }
        
        return results


if __name__ == "__main__":
    cli = VolumeCLI()
    
    print("[Volume Analysis] Ready")
    print("Use: python pt_volume.py BTC 2024-01-01 2024-12-31")
