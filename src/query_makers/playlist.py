"""Playlist query maker for YouTube API requests."""

from resource_ids.playlist_id import PlaylistId
from .resource import ResourceQueryMaker


class PlaylistQueryMaker(ResourceQueryMaker):
    """Query maker for playlist resources."""

    def __init__(self, parts: str):
        super().__init__("playlists", parts, PlaylistId)
