"""Query maker for YouTube API requests."""

from __future__ import annotations

from typing import Dict, List, Tuple

from config import YOUTUBE_API_BASE

class QueryMaker:
    """Base class for creating YouTube API queries."""

    def __init__(self, parts: str):
        self.parts = parts

    def make_query(self, resource_ids: List[str], api_key: str, max_results: int = 50) -> Tuple[str, Dict]:
        """Create a query for the given resource IDs."""
        raise NotImplementedError("This method should be implemented by subclasses.")

class VideoQueryMaker(QueryMaker):
    """Query maker for video resources."""

    def make_query(self, video_ids: List[str], api_key: str, max_results: int = 50) -> Tuple[str, Dict]:
        """Create a query for videos."""
        url = f"{YOUTUBE_API_BASE}/videos"
        params = {
            "part": self.parts,
            "id": ",".join(video_ids),
            "key": api_key,
            "maxResults": max_results,
        }
        return url, params

class PlaylistQueryMaker(QueryMaker):
    """Query maker for playlist resources."""

    def make_query(self, playlist_ids: List[str], api_key: str, max_results: int = 50) -> Tuple[str, Dict]:
        """Create a query for playlists."""
        url = f"{YOUTUBE_API_BASE}/playlists"
        params = {
            "part": self.parts,
            "id": ",".join(playlist_ids),
            "key": api_key,
            "maxResults": max_results,
        }
        return url, params

class ChannelQueryMaker(QueryMaker):
    """Query maker for channel resources."""

    def make_query(self, channel_ids: List[str], api_key: str, max_results: int = 50) -> Tuple[str, Dict]:
        """Create a query for channels."""
        url = f"{YOUTUBE_API_BASE}/channels"
        params = {
            "part": self.parts,
            "id": ",".join(channel_ids),
            "key": api_key,
            "maxResults": max_results,
        }
        return url, params

__all__ = ["QueryMaker", "VideoQueryMaker", "PlaylistQueryMaker", "ChannelQueryMaker"]