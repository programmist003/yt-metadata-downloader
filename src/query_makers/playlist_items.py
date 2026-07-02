"""Playlist items query maker for YouTube API requests."""

from resource_ids.playlist_id import PlaylistId
from .resource import ResourceQueryMaker


class PlaylistItemsQueryMaker(ResourceQueryMaker):
    """Query maker for playlist items resources."""

    def __init__(self, parts: str):
        super().__init__("playlistItems", parts, PlaylistId)
