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


def videos_spec(ids: List[str], api_key: str, parts: str) -> Tuple[str, Dict]:
    url = f"{YOUTUBE_API_BASE}/videos"
    params = {"part": parts, "id": ",".join(ids), "key": api_key}
    return url, params


def playlists_spec(ids: List[str], api_key: str, parts: str) -> Tuple[str, Dict]:
    url = f"{YOUTUBE_API_BASE}/playlists"
    params = {"part": parts, "id": ",".join(ids), "key": api_key}
    return url, params


def channels_spec(ids: List[str], api_key: str, parts: str) -> Tuple[str, Dict]:
    url = f"{YOUTUBE_API_BASE}/channels"
    params = {"part": parts, "id": ",".join(ids), "key": api_key}
    return url, params


def playlistitems_spec(
    playlist_id: str,
    api_key: str,
    parts: str,
    max_results: int = 50,
    page_token: str | None = None,
) -> Tuple[str, Dict]:
    url = f"{YOUTUBE_API_BASE}/playlistItems"
    params = {
        "part": parts,
        "playlistId": playlist_id,
        "maxResults": max_results,
        "key": api_key,
    }
    if page_token:
        params["pageToken"] = page_token
    return url, params


__all__ = [
    "QueryMaker",
    "VideoQueryMaker",
    "PlaylistQueryMaker",
    "ChannelQueryMaker",
    "videos_spec",
    "playlists_spec",
    "channels_spec",
    "playlistitems_spec",
]
