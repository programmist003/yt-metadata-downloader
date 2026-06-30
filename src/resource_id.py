"""Resource identifiers for different types of YouTube resources."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Type

from query_maker import QueryMaker, VideoQueryMaker, PlaylistQueryMaker, ChannelQueryMaker

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

@dataclass
class VideoId(ResourceId):
    """Identifier for video resources."""

    def __init__(self, value: str):
        super().__init__(value=value, kind="youtube#video", query_maker=VideoQueryMaker("contentDetails,id,snippet,statistics,status"))

@dataclass
class PlaylistId(ResourceId):
    """Identifier for playlist resources."""

    def __init__(self, value: str):
        super().__init__(value=value, kind="youtube#playlist", query_maker=PlaylistQueryMaker("contentDetails,id,snippet,status"))

@dataclass
class ChannelId(ResourceId):
    """Identifier for channel resources."""

    def __init__(self, value: str):
        super().__init__(value=value, kind="youtube#channel", query_maker=ChannelQueryMaker("snippet,contentDetails,statistics"))

__all__ = ["ResourceId", "VideoId", "PlaylistId", "ChannelId"]