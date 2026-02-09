"""
Hardened Logging System for PowerTrader AI
Version: 2.1.0
Updated: 2026-02-08

Refactored for millisecond precision, line-number traceability, 
and 48-hour time-based rotation.
"""

import logging
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from logging.handlers import TimedRotatingFileHandler
import threading


@dataclass
class LogConfig:
    log_level: str = "INFO"
    log_file: str = "hub_data/powertrader.log"
    max_log_size_mb: int = 10
    backup_log_count: int = 2  # Maintains 48 hours (2 x 24h)
    enable_console: bool = True
    enable_json: bool = True
    critical_notification: bool = True
    debug_mode: bool = False 


class StructuredFormatter(logging.Formatter):
    """Formatter for persistent JSON logs."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "module": record.name,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
        }

        if hasattr(record, "extra"):
            log_entry["extra"] = record.extra

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


class DebugConsoleFormatter(logging.Formatter):
    """
    Enhanced console formatter with milliseconds and line numbers.
    """

    def format(self, record: logging.LogRecord) -> str:
        # Millisecond precision for diagnosing race conditions
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        level = record.levelname
        module = record.name
        message = record.getMessage()

        color_map = {
            "DEBUG": "\033[36m",    # Cyan
            "INFO": "\033[32m",     # Green
            "WARNING": "\033[33m",  # Yellow
            "ERROR": "\033[31m",    # Red
            "CRITICAL": "\033[35m", # Magenta
        }
        reset = "\033[0m"
        level_color = color_map.get(level, "")

        return f"{timestamp} {level_color}[{level}]{reset} [{module}:{record.lineno}] {message}"


class StructuredLogger:
    """Singleton logger with integrated 48-hour rotation logic."""

    _instances = {}
    _lock = threading.Lock()

    def __new__(cls, name: str, *args, **kwargs):
        with cls._lock:
            if name not in cls._instances:
                cls._instances[name] = super(StructuredLogger, cls).__new__(cls)
            return cls._instances[name]

    def __init__(self, name: str, config: Optional[LogConfig] = None):
        if hasattr(self, 'initialized'):
            return
        self.name = name
        self.config = config or LogConfig()
        self.logger = logging.getLogger(name)
        
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False
        self._setup_handlers()
        self.initialized = True

    def _setup_handlers(self) -> None:
        """Configures handlers for time-based rotation and console output."""
        self.logger.handlers.clear()

        log_path = Path(self.config.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # 1. Permanent JSON File Handler with 48-Hour Retention
        if self.config.enable_json:
            # Rotates every 1 Day ('D'), keeps 2 backups (total 48h)
            fh = TimedRotatingFileHandler(
                log_path,
                when='D',
                interval=1,
                backupCount=2,
                encoding='utf-8'
            )
            fh.setFormatter(StructuredFormatter())
            fh.setLevel(logging.INFO)
            self.logger.addHandler(fh)

        # 2. Live Debug Console Handler
        if self.config.enable_console:
            ch = logging.StreamHandler(sys.stdout)
            ch.setFormatter(DebugConsoleFormatter())
            # Switch between INFO and DEBUG based on config
            ch.setLevel(logging.DEBUG if self.config.debug_mode else logging.INFO)
            self.logger.addHandler(ch)

    def debug(self, msg: str): self.logger.debug(msg)
    def info(self, msg: str): self.logger.info(msg)
    def warning(self, msg: str): self.logger.warning(msg)
    def error(self, msg: str): self.logger.error(msg, exc_info=True)
    def critical(self, msg: str): self.logger.critical(msg, exc_info=True)


def get_logger(name: str) -> StructuredLogger:
    """Retrieves logger instance with hot-reloaded settings."""
    from pt_config import get_config
    conf = get_config().get()
    
    # Map configuration settings to logger config
    log_config = LogConfig(
        log_level=conf.system.log_level,
        log_file=conf.system.log_file,
        debug_mode=conf.system.debug_mode
    )
    return StructuredLogger(name, log_config)