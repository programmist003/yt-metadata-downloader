"""Query maker for YouTube API requests."""

from __future__ import annotations

from typing import Dict, List, Tuple

from config import YOUTUBE_API_BASE


class QueryMaker:
    """Base class for creating YouTube API queries."""

    def __init__(self, parts: str):
        self.parts = parts

    def make_query(
        self, resource_ids: List[str], api_key: str, max_results: int = 50
    ) -> Tuple[str, Dict]:
        """Create a query for the given resource IDs."""
        raise NotImplementedError("This method should be implemented by subclasses.")


class ResourceQueryMaker(QueryMaker):
    """Query maker for resource resources."""

    def __init__(self, resource_type: str, parts: str):
        super().__init__(parts)
        self.resource_type = resource_type

    def make_query(
        self, resource_ids: List[str], api_key: str, max_results: int = 50
    ) -> Tuple[str, Dict]:
        """Create a query for the given resource IDs."""
        url = f"{YOUTUBE_API_BASE}/{self.resource_type}"
        params = {
            "part": self.parts,
            "id": ",".join(resource_ids),
            "key": api_key,
            "maxResults": max_results,
        }
        return url, params


class VideoQueryMaker(ResourceQueryMaker):
    """Query maker for video resources."""

    def __init__(self, parts: str):
        super().__init__("videos", parts)


class PlaylistQueryMaker(ResourceQueryMaker):
    """Query maker for playlist resources."""

    def __init__(self, parts: str):
        super().__init__("playlists", parts)


class ChannelQueryMaker(ResourceQueryMaker):
    """Query maker for channel resources."""

    def __init__(self, parts: str):
        super().__init__("channels", parts)


__all__ = ["QueryMaker", "VideoQueryMaker", "PlaylistQueryMaker", "ChannelQueryMaker"]
