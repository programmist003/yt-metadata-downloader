"""Video query maker for YouTube API requests."""

from resource_ids.video_id import VideoId
from .resource import ResourceQueryMaker


class VideoQueryMaker(ResourceQueryMaker):
    """Query maker for video resources."""

    def __init__(self, parts: str):
        super().__init__("videos", parts, VideoId)
