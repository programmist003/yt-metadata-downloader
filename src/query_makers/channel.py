"""Channel query maker for YouTube API requests."""

from resource_ids.channel_id import ChannelId
from resource_ids.channel_handle import ChannelHandle
from resource_ids.channel_custom import ChannelCustom
from .resource import ResourceQueryMaker


class ChannelQueryMaker(ResourceQueryMaker):
    """Query maker for channel resources."""

    def __init__(self, parts: str):
        super().__init__("channels", parts, (ChannelId, ChannelHandle, ChannelCustom))
