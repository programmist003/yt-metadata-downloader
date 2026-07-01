"""Channel query maker for YouTube API requests."""

from .resource import ResourceQueryMaker


class ChannelQueryMaker(ResourceQueryMaker):
    """Query maker for channel resources."""

    def __init__(self, parts: str):
        super().__init__("channels", parts)