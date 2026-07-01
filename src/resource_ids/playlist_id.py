from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, List, Union
from urllib.parse import parse_qs

from query_maker import (
    PlaylistQueryMaker,
)
from resource_ids.resource_id import ResourceId
from url import URL
from utils import is_youtube_url


@dataclass
class PlaylistId(ResourceId):
    """Identifier for playlist resources."""

    def __init__(self, value: str):
        super().__init__(
            value=value,
            kind="youtube#playlist",
            query_maker=PlaylistQueryMaker("contentDetails,id,snippet,status"),
        )

    @classmethod
    def _parse_playlist_from_query(
        cls, url_obj: URL
    ) -> Optional[Dict[str, Union[str, None]]]:
        """Parse playlist ID from query parameters."""
        if url_obj.query:
            query_params = parse_qs(url_obj.query)
            if "list" in query_params and query_params["list"]:
                return {
                    "type": "playlist",
                    "raw": str(url_obj),
                    "identifier": query_params["list"][0],
                }
        return None

    @classmethod
    def _parse_playlist_url(cls, url_str: str) -> Optional[Dict[str, Union[str, None]]]:
        """Parse a YouTube playlist URL and extract playlist ID."""
        try:
            url_obj = URL.parse(url_str)
        except ValueError:
            return None

        # Check if the URL is from YouTube using is_youtube_url
        if not is_youtube_url(url_obj):
            return None

        # Try parsing the playlist ID from query parameters
        return cls._parse_playlist_from_query(url_obj)

    @classmethod
    def from_urls(cls, urls: List[str]) -> List[Union[PlaylistId, None]]:
        """Create a list of PlaylistId from a list of URLs."""
        playlist_ids: List[Union[PlaylistId, None]] = []
        for url in urls:
            parsed = cls._parse_playlist_url(url)
            if parsed and parsed.get("type") == "playlist":
                playlist_ids.append(cls(value=parsed["identifier"])) # type: ignore
            else:
                playlist_ids.append(None)
        return playlist_ids
