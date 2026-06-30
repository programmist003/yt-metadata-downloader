"""Authentication module"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import toml

DEFAULT_CONFIG_PATH = Path("config.toml")

def load_api_key(config_path: Path | str = DEFAULT_CONFIG_PATH) -> Optional[str]:
    """Load YouTube API key from a TOML config file."""
    try:
        path = Path(config_path)
        if not path.exists():
            return None

        config = toml.load(path)
        return config.get("api_key")
    except Exception as e:
        print(f"Error loading API key: {e}")
        return None

__all__ = ["load_api_key"]

