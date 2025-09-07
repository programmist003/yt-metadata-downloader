"""YouTube video resource kind module"""

from icecream import ic  # pylint: disable=unused-import
from furl import furl
from kinds.kind import Kind
from properties.data_getter import DataGetter
from properties.resource_id_getter import ResourceIdGetter
from utils import check_domain, prepare_list_method_method
from auth import youtube


class Video(Kind):
    """YouTube video resource kind"""
    _properties: dict[type, object] = dict()
    def __init__(self, *properties: list):
        self.add(ResourceIdGetter(get_video_id))
        self.add(
            DataGetter(
                prepare_list_method_method(
                    youtube.videos(),  # type: ignore # pylint: disable=no-member
                    "contentDetails, id, liveStreamingDetails, "
                    "localizations, paidProductPlacementDetails, player, "
                    "recordingDetails, snippet, statistics, status, topicDetails",
                )
            )
        )
        super().__init__(*properties)


def get_video_id(url: str) -> str | None:
    """Get video ID from a YouTube URL"""
    f = furl(url)
    if not check_domain(url) or f.path != "/watch":
        return None
    return f.args.get("v")
