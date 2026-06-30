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


def parse_url(url: str) -> dict:
    """Parse YouTube URL and return resource info.

    Returns dict with:
      - type: one of 'channel_id','channel_custom','channel_handle','video','playlist','other'
      - raw: original URL
      - identifier: extracted id or name (without leading @), or None
    """
    p = urlparse(url)
    host = (p.netloc or "").lower()
    path = p.path or ""
    query = parse_qs(p.query or "")

    def mk(t: str, ident: Optional[str]):
        return {"type": t, "raw": url, "identifier": ident}

    # Accept common youtube hosts
    if not any(h in host for h in ("youtube.com", "youtu.be")):
        return mk("other", None)

    # Short youtu.be links: path is /<videoId>
    if "youtu.be" in host:
        vid = path.lstrip("/")
        return mk("video", vid if vid else None)

    # video by query v= or embed
    if "v" in query and query["v"]:
        return mk("video", query["v"][0])
    m = re.match(r"^/embed/([^/]+)", path)
    if m:
        return mk("video", m.group(1))

    # playlist by list=
    if "list" in query and query["list"]:
        return mk("playlist", query["list"][0])

    # /playlist path with query handled above; continue to channel/video patterns
    # channel by id: /channel/<id>
    m = re.match(r"^/channel/([^/]+)", path)
    if m:
        return mk("channel_id", m.group(1))

    # custom channel: /c/<name> or /user/<name>
    m = re.match(r"^/c/([^/]+)", path)
    if m:
        return mk("channel_custom", m.group(1))
    m = re.match(r"^/user/([^/]+)", path)
    if m:
        return mk("channel_custom", m.group(1))

    # handle: /@handle or segments containing @handle
    m = re.match(r"^/@([^/]+)", path)
    if m:
        return mk("channel_handle", m.group(1))
    m = re.search(r"/@([^/]+)", path)
    if m:
        return mk("channel_handle", m.group(1))

    # Fallback: if path looks like a channel handle without leading @ (rare)
    m = re.match(r"^/([A-Za-z0-9_\-]+)/?$", path)
    if m:
        # ambiguous: could be root page; treat as 'other'
        return mk("other", None)

    return mk("other", None)


def resolve_channel_id(
    parsed: Dict[str, Optional[str]], api_key: str, timeout: int = 30
) -> Optional[str]:
    """Resolve a parsed URL dict (from `parse_url`) to a `channelId`.

    Returns `channelId` string on success or `None` when not resolvable.
    """
    if not parsed:
        return None

    t = parsed.get("type")
    ident = parsed.get("identifier")

    # If it's already a channel ID, return it directly
    if t == "channel_id":
        return ident

    import requests
    import sys

    params = {"part": "id", "key": api_key}

    if t == "channel_handle":
        if not ident:
            return None
        # API accepts handle with or without '@'; send without leading @ for consistency
        handle = ident[1:] if ident.startswith("@") else ident
        params["forHandle"] = handle
    elif t == "channel_custom":
        if not ident:
            return None
        params["forUsername"] = ident
    else:
        return None

    url = f"{YOUTUBE_API_BASE}/channels"
    headers = {"User-Agent": "yt-metadata-downloader/1.0"}

    try:
        resp = requests.get(url, params=params, timeout=timeout, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("items", [])
        if not items:
            return None
        # items[0].get('id') is the channelId
        return items[0].get("id")
    except requests.RequestException as e:
        sys.stderr.write(f"Failed to resolve channel id for {parsed!r}: {e}\n")
        sys.stderr.flush()
        return None


def resolve_channel_id_from_url(
    url: str, api_key: str, timeout: int = 30
) -> Optional[str]:
    parsed = parse_url(url)
    return resolve_channel_id(parsed, api_key, timeout=timeout)


@dataclass
class ResourceId():
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
    def from_urls(cls, urls: List[str]) -> List[Union[VideoId, None]]:
        """Create a list of VideoId from a list of URLs."""
        video_ids: List[Union[VideoId, None]] = []
        for url in urls:
            parsed = parse_url(url)
            if parsed and parsed.get("type") == "video":
                video_ids.append(cls(value=parsed["identifier"]))
            else:
                video_ids.append(None)
        return video_ids


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
    def from_urls(cls, urls: List[str]) -> List[Union[PlaylistId, None]]:
        """Create a list of PlaylistId from a list of URLs."""
        playlist_ids: List[Union[PlaylistId, None]] = []
        for url in urls:
            parsed = parse_url(url)
            if parsed and parsed.get("type") == "playlist":
                playlist_ids.append(cls(value=parsed["identifier"]))
            else:
                playlist_ids.append(None)
        return playlist_ids


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
    def from_urls(cls, urls: List[str]) -> List[Union[ChannelId, None]]:
        """Create a list of ChannelId from a list of URLs."""
        channel_ids: List[Union[ChannelId, None]] = []
        for url in urls:
            parsed = parse_url(url)
            if parsed and parsed.get("type") in (
                "channel_id",
                "channel_custom",
                "channel_handle",
            ):
                channel_ids.append(cls(value=parsed["identifier"]))
            else:
                channel_ids.append(None)
        return channel_ids


__all__ = [
    "ResourceId",
    "VideoId",
    "PlaylistId",
    "ChannelId",
    "parse_url",
    "resolve_channel_id",
    "resolve_channel_id_from_url",
]
