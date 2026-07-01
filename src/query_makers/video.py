"""Video query maker for YouTube API requests."""

from .resource import ResourceQueryMaker


class VideoQueryMaker(ResourceQueryMaker):
    """Query maker for video resources."""

    def __init__(self, parts: str):
        super().__init__("videos", parts)