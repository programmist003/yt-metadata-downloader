"""Resource identifiers for different types of YouTube resources."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, List, Union
from urllib.parse import urlparse, parse_qs
import re

from config import YOUTUBE_API_BASE
from query_maker import (
    QueryMaker,
    VideoQueryMaker,
    PlaylistQueryMaker,
    ChannelQueryMaker,
)


class URLParser:
    """Parser for YouTube URLs."""

    def __init__(self, url: str):
        self.url = url
        self.parsed = urlparse(url)
        self.host = (self.parsed.netloc or "").lower()
        self.path = self.parsed.path or ""
        self.query = parse_qs(self.parsed.query or "")



    def parse(self) -> dict:
        """Parse the URL and return resource info.

        Returns dict with:
          - type: one of 'channel_id','channel_custom','channel_handle','video','playlist','other'
          - raw: original URL
          - identifier: extracted id or name (without leading @), or None
        """
        if not self._is_youtube_host():
            return {"type": "other", "raw": self.url, "identifier": None}
        # Short youtu.be links: path is /<videoId>
        if "youtu.be" in self.host:
            return self._parse_short_video_url()

        # video by query v= or embed
        video_result = self._parse_video_from_query()
        if video_result:
            return video_result
        video_result = self._parse_video_from_embed()
        if video_result:
            return video_result

        # playlist by list=
        playlist_result = self._parse_playlist_from_query()
        if playlist_result:
            return playlist_result

        # channel by id: /channel/<id>
        channel_id_result = self._parse_channel_id()
        if channel_id_result:
            return channel_id_result

        # custom channel: /c/<name> or /user/<name>
        custom_channel_result = self._parse_custom_channel()
        if custom_channel_result:
            return custom_channel_result

        # handle: /@handle or segments containing @handle
        channel_handle_result = self._parse_channel_handle()
        if channel_handle_result:
            return channel_handle_result

        # Fallback: if path looks like a channel handle without leading @ (rare)
        fallback_result = self._parse_fallback()
        if fallback_result:
            return fallback_result

        return {"type": "other", "raw": self.url, "identifier": None}


def parse_url(url: str) -> dict:
    """Parse YouTube URL and return resource info.

    Returns dict with:
      - type: one of 'channel_id','channel_custom','channel_handle','video','playlist','other'
      - raw: original URL
      - identifier: extracted id or name (without leading @), or None
    """
    parser = URLParser(url)
    return parser.parse()


@dataclass
class ResourceId:
    """Base class for resource identifiers."""

    value: str
    kind: str
    query_maker: QueryMaker

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ResourceId):
            return False
        return self.value == other.value and self.kind == other.kind

    def to_dict(self) -> Dict[str, str]:
        """Convert the resource ID to a dictionary."""
        return {
            "value": self.value,
            "kind": self.kind,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, str], query_maker: QueryMaker) -> ResourceId:
        """Create a resource ID from a dictionary."""
        return cls(value=data["value"], kind=data["kind"], query_maker=query_maker)

    @classmethod
    def from_urls(cls, urls: List[str]) -> List[Union[ResourceId, None]]:
        """Create a list of ResourceId from a list of URLs."""
        pass


__all__ = [
    "ResourceId",
    "VideoId",
    "PlaylistId",
    "ChannelId",
    "ChannelHandle",
    "ChannelCustom",
    "parse_url",
]
