"""Package for handling YouTube resource identifiers.

This package provides classes for parsing and managing identifiers of various
YouTube resources such as videos, playlists, and channels. It includes support
for different URL formats and provides a consistent interface for working with
resource identifiers.

Example:
    >>> from resource_ids import VideoId, PlaylistId, ChannelId
    >>> video_id = VideoId.from_urls(["https://youtu.be/dQw4w9WgXcQ"])[0]
    >>> print(video_id)
"""

from .resource_id import ResourceId, ResourceIdBase
from .video_id import VideoId
from .playlist_id import PlaylistId
from .channel_id import ChannelId
from .channel_handle import ChannelHandle
from .channel_custom import ChannelCustom

__all__ = [
    "ResourceId",
    "ResourceIdBase",
    "VideoId",
    "PlaylistId",
    "ChannelId",
    "ChannelHandle",
    "ChannelCustom",
]
