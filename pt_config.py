"""
Unified Configuration Management for PowerTrader AI
Updated: 2026-02-08
"""
import os
import yaml
import json
import logging
import threading
import hashlib
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict, Any

@dataclass
class SystemConfig:
    log_level: str = "INFO"
    log_file: str = "hub_data/powertrader.log"
    max_log_size_mb: int = 10
    backup_log_count: int = 5
    debug_mode: bool = False
    log_retention_hours: int = 48  # Added for time-based rotation logic

@dataclass
class PowerTraderConfig:
    trading: Any = None
    notifications: Any = None
    exchanges: Any = None
    analytics: Any = None
    position_sizing: Any = None
    correlation: Any = None
    system: SystemConfig = field(default_factory=SystemConfig)

    def __post_init__(self):
        # Default initialization for missing sections
        if self.system is None:
            self.system = SystemConfig()

class ConfigManager:
    """Thread-safe configuration manager with hot-reload and environment overrides."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ConfigManager, cls).__new__(cls)
            return cls._instance

    def __init__(self, config_dir: Optional[str] = None):
        if hasattr(self, 'initialized'): return
        self.config_dir = Path(config_dir or os.getcwd())
        self.config_path = self.config_dir / "config.yaml"
        self._config: Optional[PowerTraderConfig] = None
        self._last_hash = None
        self._callbacks = []
        
        self.reload()
        self.initialized = True

    def _get_hash(self, data: Dict) -> str:
        """Calculate config hash for change detection."""
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def reload(self) -> bool:
        """Reloads YAML and merges environment overrides."""
        try:
            data = {}
            if self.config_path.exists():
                with open(self.config_path, "r") as f:
                    data = yaml.safe_load(f) or {}

            # Environment Override for Debug Mode
            env_debug = os.getenv("POWERTRADER_SYSTEM_DEBUG_MODE", "").lower()
            if env_debug in ("true", "1", "yes"):
                if "system" not in data: data["system"] = {}
                data["system"]["debug_mode"] = True

            new_hash = self._get_hash(data)
            if new_hash == self._last_hash: return False

            self._config = self._dict_to_config(data)
            self._last_hash = new_hash
            
            # Notify registered modules (like pt_logging) of the update
            for cb in self._callbacks: cb(self._config)
            return True
        except Exception as e:
            print(f"Config Reload Error: {e}")
            return False

    def _dict_to_config(self, data: Dict[str, Any]) -> PowerTraderConfig:
        """Maps dictionary data to the PowerTraderConfig dataclass structure."""
        system_data = data.get("system", {})
        # Ensure system settings are properly typed
        system_cfg = SystemConfig(**system_data) if isinstance(system_data, dict) else SystemConfig()
        
        return PowerTraderConfig(
            trading=data.get("trading"),
            notifications=data.get("notifications"),
            exchanges=data.get("exchanges"),
            analytics=data.get("analytics"),
            system=system_cfg
        )

    def get(self) -> PowerTraderConfig:
        """Returns the current validated configuration."""
        return self._config

    def register_callback(self, callback):
        """Register a function to be called when configuration changes."""
        self._callbacks.append(callback)

def get_config() -> ConfigManager:
    """Singleton access to the ConfigManager."""
    return ConfigManager()