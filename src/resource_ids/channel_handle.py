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
class ChannelHandle(ResourceId):
    """Identifier for channel handle resources."""

    def __init__(self, value: str):
        super().__init__(
            value=value,
            kind="youtube#channel",
            query_maker=ChannelQueryMaker("snippet,contentDetails,statistics"),
        )

    @classmethod
    def _parse_channel_handle(
        cls, url_obj: URL
    ) -> Optional[Dict[str, Union[str, None]]]:
        """Parse channel handle from path."""
        m = re.match(r"^/@([^/]+)", url_obj.path)
        if m:
            return {
                "type": "channel_handle",
                "raw": str(url_obj),
                "identifier": m.group(1),
            }
        m = re.search(r"/@([^/]+)", url_obj.path)
        if m:
            return {
                "type": "channel_handle",
                "raw": str(url_obj),
                "identifier": m.group(1),
            }
        return None

    @classmethod
    def _parse_channel_handle_url(
        cls, url_str: str
    ) -> Optional[Dict[str, Union[str, None]]]:
        """Parse a YouTube channel handle URL and extract handle."""
        try:
            url_obj = URL.parse(url_str)
        except ValueError:
            return None

        # Check if the URL is from YouTube
        if not is_youtube_url(url_obj):
            return None

        # Try parsing the channel handle from path
        return cls._parse_channel_handle(url_obj)

    @classmethod
    def from_urls(cls, urls: List[str]) -> List[Union[ChannelHandle, None]]:
        """Create a list of ChannelHandle from a list of URLs."""
        channel_handles: List[Union[ChannelHandle, None]] = []
        for url in urls:
            parsed = cls._parse_channel_handle_url(url)
            if parsed and parsed.get("type") == "channel_handle":
                channel_handles.append(cls(value=parsed["identifier"])) # type: ignore
            else:
                channel_handles.append(None)
        return channel_handles
