import json
from pathlib import Path
from typing import Dict, Any


class Settings:
    def __init__(self):
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from config.json"""
        config_path = Path(__file__).parent.parent.parent.parent / "config.json"
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON in config.json")

    @property
    def config(self) -> Dict[str, Any]:
        """Get the configuration dictionary"""
        return self._config

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key"""
        return self._config.get(key, default)


settings = Settings()