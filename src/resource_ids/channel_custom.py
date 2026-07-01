from dataclasses import dataclass
from typing import List, Union, Optional, Dict
import re

from resource_ids.resource_id import ResourceId
from query_maker import ChannelQueryMaker
from url import URL
from utils import is_youtube_url


@dataclass
class ChannelCustom(ResourceId):
    """Identifier for custom channel resources."""

    def __init__(self, value: str):
        super().__init__(
            value=value,
            kind="youtube#channel",
            query_maker=ChannelQueryMaker("snippet,contentDetails,statistics"),
        )

    @classmethod
    def _parse_custom_channel(
        cls, url_obj: URL
    ) -> Optional[Dict[str, Union[str, None]]]:
        """Parse custom channel name from path."""
        m = re.match(r"^/c/([^/]+)", url_obj.path)
        if m:
            return {
                "type": "channel_custom",
                "raw": str(url_obj),
                "identifier": m.group(1),
            }
        m = re.match(r"^/user/([^/]+)", url_obj.path)
        if m:
            return {
                "type": "channel_custom",
                "raw": str(url_obj),
                "identifier": m.group(1),
            }
        return None

    @classmethod
    def _parse_custom_channel_url(
        cls, url_str: str
    ) -> Optional[Dict[str, Union[str, None]]]:
        """Parse a YouTube custom channel URL and extract custom name."""
        try:
            url_obj = URL.parse(url_str)
        except ValueError:
            return None

        # Check if the URL is from YouTube
        if not is_youtube_url(url_obj):
            return None

        # Try parsing the custom channel name from path
        return cls._parse_custom_channel(url_obj)

    @classmethod
    def from_urls(cls, urls: List[str]) -> List[Union["ChannelCustom", None]]:
        """Create a list of ChannelCustom from a list of URLs."""
        channel_customs: List[Union[ChannelCustom, None]] = []
        for url in urls:
            parsed = cls._parse_custom_channel_url(url)
            if parsed and parsed.get("type") == "channel_custom":
                channel_customs.append(cls(value=parsed["identifier"])) # type: ignore
            else:
                channel_customs.append(None)
        return channel_customs
