"""
Multi-Asset Correlation Analysis Module for PowerTrader AI
Updated for safe database concurrency and portfolio weighting.
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from contextlib import contextmanager

@dataclass
class CorrelationMetrics:
    symbol_a: str
    symbol_b: str
    correlation: float
    p_value: float
    timestamp: datetime
    timeframe: str

@dataclass
class CorrelationAlert:
    symbol_a: str
    symbol_b: str
    correlation: float
    threshold: float
    timestamp: datetime
    alert_type: str 

class CorrelationAnalyzer:
    """Analyzes correlation between multiple trading pairs with safe concurrency."""

    def __init__(self, db_path: str):
        self.db_path = db_path

    @contextmanager
    def _safe_conn(self):
        """Context manager with timeout to prevent 'database locked' errors."""
        conn = sqlite3.connect(self.db_path, timeout=15)
        try:
            yield conn
        finally:
            conn.close()

    def calculate_correlation_matrix(
        self, symbols: List[str], timeframe_days: int = 30, min_data_points: int = 20
    ) -> Dict[str, Dict[str, float]]:
        """Calculate correlation matrix using a safe, temporary connection."""
        correlation_matrix = {}

        with self._safe_conn() as conn:
            cursor = conn.cursor()
            for i, symbol_a in enumerate(symbols):
                correlation_matrix[symbol_a] = {}
                for j, symbol_b in enumerate(symbols):
                    if i == j:
                        correlation_matrix[symbol_a][symbol_b] = 1.0
                        continue

                    try:
                        query = """
                            SELECT timestamp, close_price FROM trade_exits 
                            WHERE symbol = ? AND timestamp >= datetime('now', ?)
                            ORDER BY timestamp DESC LIMIT 1000
                        """
                        lookback = f'-{timeframe_days} days'
                        
                        df_a = pd.read_sql_query(query, conn, params=(symbol_a, lookback))
                        df_b = pd.read_sql_query(query, conn, params=(symbol_b, lookback))

                        df_merged = pd.merge(df_a, df_b, on="timestamp", how="inner").dropna()

                        if len(df_merged) >= min_data_points:
                            correlation = df_merged['close_price_x'].pct_change().corr(
                                df_merged['close_price_y'].pct_change()
                            )
                            correlation_matrix[symbol_a][symbol_b] = correlation if not pd.isna(correlation) else 0.0
                        else:
                            correlation_matrix[symbol_a][symbol_b] = 0.0

                    except Exception as e:
                        print(f"[Correlation] Error between {symbol_a}/{symbol_b}: {e}")
                        correlation_matrix[symbol_a][symbol_b] = 0.0

        return correlation_matrix

    def get_current_correlations(
        self, symbols: List[str], threshold: float = 0.8, lookback_days: int = 30
    ) -> List[CorrelationAlert]:
        alerts = []
        matrix = self.calculate_correlation_matrix(symbols, lookback_days)

        for symbol_a in symbols:
            for symbol_b in symbols:
                if symbol_a == symbol_b: continue
                val = matrix[symbol_a].get(symbol_b, 0.0)
                if val >= threshold:
                    alerts.append(CorrelationAlert(
                        symbol_a=symbol_a, symbol_b=symbol_b, correlation=val,
                        threshold=threshold, timestamp=datetime.now(), alert_type="HIGH_CORRELATION"
                    ))
        return alerts

def calculate_portfolio_correlation(
    db_path: str,
    portfolio: Dict[str, float],
    symbols: Optional[List[str]] = None,
    correlation_threshold: float = 0.8,
) -> Dict[str, float]:
    """
    Exported function to calculate current portfolio correlation.
    Fixes the ImportError in pt_risk_dashboard.py.
    """
    if not symbols:
        symbols = list(portfolio.keys())

    analyzer = CorrelationAnalyzer(db_path)
    correlation_matrix = analyzer.calculate_correlation_matrix(symbols)

    portfolio_correlation = {}
    total_value = sum(portfolio.values())

    for symbol in symbols:
        weight = portfolio.get(symbol, 0) / total_value if total_value > 0 else 0
        weighted_avg = 0.0
        weight_sum = 0.0

        for other_symbol in symbols:
            if symbol != other_symbol:
                correlation = correlation_matrix[symbol].get(other_symbol, 0.0)
                weighted_avg += correlation * weight
                weight_sum += weight

        if weight_sum > 0:
            portfolio_correlation[symbol] = weighted_avg / weight_sum

    return portfolio_correlation

if __name__ == "__main__":
    # Test block
    print("Correlation logic initialized.")