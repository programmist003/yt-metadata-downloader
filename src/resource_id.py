"""Resource identifiers for different types of YouTube resources."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Type, List, Union

from query_maker import (
    QueryMaker,
    VideoQueryMaker,
    PlaylistQueryMaker,
    ChannelQueryMaker,
)
from links.parser import parse_url


@dataclass
class ResourceId(ABC):
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
    @abstractmethod
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


__all__ = ["ResourceId", "VideoId", "PlaylistId", "ChannelId"]
