"""Authentication module"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import toml
from googleapiclient.discovery import build

DEFAULT_CONFIG_PATH = Path("config.toml")


def load_api_key(config_path: Path | str = DEFAULT_CONFIG_PATH) -> Optional[str]:
    """Load YouTube API key from a TOML config file."""
    path = Path(config_path)
    if not path.exists():
        return None

    config = toml.load(path)
    return config.get("api_key")


def create_youtube_client(
    developer_key: Optional[str] = None, config_path: Path | str = DEFAULT_CONFIG_PATH
):
    """Create a YouTube API client from a developer key or config file."""
    if developer_key is None:
        developer_key = load_api_key(config_path)

    if not developer_key:
        raise ValueError(
            f"YouTube API key is required but was not found in '{config_path}'"
        )

    return build("youtube", "v3", developerKey=developer_key)


class YouTubeClientProxy:
    """Proxy object for deferred YouTube API client initialization."""

    def __init__(
        self,
        developer_key: Optional[str] = None,
        config_path: Path | str = DEFAULT_CONFIG_PATH,
    ):
        self._developer_key = developer_key
        self._config_path = Path(config_path)
        self._client = None

    def _ensure_client(self):
        if self._client is None:
            self._client = create_youtube_client(self._developer_key, self._config_path)
        return self._client

    def set_api_key(self, developer_key: str) -> None:
        self._developer_key = developer_key
        self._client = None

    def __getattr__(self, name: str):
        return getattr(self._ensure_client(), name)

    def __repr__(self) -> str:
        return f"<YouTubeClientProxy key={'set' if self._developer_key else 'unset'} config={self._config_path}>"


youtube = YouTubeClientProxy()


def set_api_key(developer_key: str) -> None:
    """Set the YouTube API key for the shared client proxy."""
    youtube.set_api_key(developer_key)


__all__ = ["load_api_key", "create_youtube_client", "set_api_key", "youtube"]
