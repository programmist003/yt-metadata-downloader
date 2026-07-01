from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, List, Union
from urllib.parse import parse_qs
import re

from query_maker import VideoQueryMaker
from resource_ids.resource_id import ResourceId
from url import URL


@dataclass
class VideoId(ResourceId):
    """Identifier for video resources."""

    def __init__(self, value: str):
        super().__init__(
            value=value,
            kind="youtube#video",
            query_maker=VideoQueryMaker("contentDetails,id,snippet,statistics,status"),
        )

    @classmethod
    def _parse_short_video_url(
        cls, url_obj: URL
    ) -> Optional[Dict[str, Union[str, None]]]:
        """Parse short YouTube URL (youtu.be)."""
        vid = url_obj.path.lstrip("/")
        if vid:
            return {"type": "video", "raw": str(url_obj), "identifier": vid}
        return None

    @classmethod
    def _parse_video_from_query(
        cls, url_obj: URL
    ) -> Optional[Dict[str, Union[str, None]]]:
        """Parse video ID from query parameters."""
        if url_obj.query:
            query_params = parse_qs(url_obj.query)
            if "v" in query_params and query_params["v"]:
                return {
                    "type": "video",
                    "raw": str(url_obj),
                    "identifier": query_params["v"][0],
                }
        return None

    @classmethod
    def _parse_video_from_embed(
        cls, url_obj: URL
    ) -> Optional[Dict[str, Union[str, None]]]:
        """Parse video ID from embed path."""
        m = re.match(r"^/embed/([^/]+)", url_obj.path)
        if m:
            return {"type": "video", "raw": str(url_obj), "identifier": m.group(1)}
        return None

    @classmethod
    def _parse_video_url(cls, url_str: str) -> Optional[Dict[str, Union[str, None]]]:
        """Parse a YouTube video URL and extract video ID."""
        try:
            url_obj = URL.parse(url_str)
        except ValueError:
            return None

        # Check if the URL is from YouTube
        if not any(
            h in url_obj.host for h in ("youtube.com", "www.youtube.com", "youtu.be")
        ):
            return None

        # Try different parsing methods
        parsers = [
            cls._parse_short_video_url,
            cls._parse_video_from_query,
            cls._parse_video_from_embed,
        ]

        for parser in parsers:
            result = parser(url_obj)
            if result:
                return result

        return None

    @classmethod
    def from_urls(cls, urls: List[str]) -> List[Union[VideoId, None]]:
        """Create a list of VideoId from a list of URLs."""
        video_ids: List[Union[VideoId, None]] = []
        for url in urls:
            parsed = cls._parse_video_url(url)
            if parsed and parsed.get("type") == "video":
                video_ids.append(cls(value=parsed["identifier"])) # type: ignore
            else:
                video_ids.append(None)
        return video_ids
