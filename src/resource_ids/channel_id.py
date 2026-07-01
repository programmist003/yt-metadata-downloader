from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, List, Union
import re

from query_maker import (
    ChannelQueryMaker,
)
from resource_ids.resource_id import ResourceId
from url import URL
from utils import is_youtube_url


@dataclass
class ChannelId(ResourceId):
    """Identifier for channel resources."""

    def __init__(self, value: str):
        super().__init__(
            value=value,
            kind="youtube#channel",
            query_maker=ChannelQueryMaker("snippet,contentDetails,statistics"),
        )

    @classmethod
    def _parse_channel_id(cls, url_obj: URL) -> Optional[Dict[str, Union[str, None]]]:
        """Parse channel ID from path."""
        m = re.match(r"^/channel/([^/]+)", url_obj.path)
        if m:
            return {
                "type": "channel_id",
                "raw": str(url_obj),
                "identifier": m.group(1),
            }
        return None

    @classmethod
    def _parse_channel_url(cls, url_str: str) -> Optional[Dict[str, Union[str, None]]]:
        """Parse a YouTube channel URL and extract channel ID."""
        try:
            url_obj = URL.parse(url_str)
        except ValueError:
            return None

        # Check if the URL is from YouTube
        if not is_youtube_url(url_obj):
            return None

        # Try parsing the channel ID from path
        return cls._parse_channel_id(url_obj)

    @classmethod
    def from_urls(cls, urls: List[str]) -> List[Union[ChannelId, None]]:
        """Create a list of ChannelId from a list of URLs."""
        channel_ids: List[Union[ChannelId, None]] = []
        for url in urls:
            parsed = cls._parse_channel_url(url)
            if parsed and parsed.get("type") == "channel_id":
                channel_ids.append(cls(value=parsed["identifier"])) # type: ignore
            else:
                channel_ids.append(None)
        return channel_ids
