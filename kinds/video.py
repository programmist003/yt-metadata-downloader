"""YouTube video resource kind module"""

import json
from icecream import ic
from toolz import partition_all
from furl import furl
from kinds.kind import Kind
from properties.data_getter import DataGetter
from properties.resource_id_getter import ResourceIdGetter
from utils import check_domain
from auth import youtube


class Video(Kind):
    """YouTube video resource kind"""

    def __init__(self, *properties: list):
        self.add(ResourceIdGetter(get_video_id))
        self.add(DataGetter(save_videos_data))
        super().__init__(*properties)


def get_video_id(url: str) -> str | None:
    """Get video ID from a YouTube URL"""
    f = furl(url)
    if not check_domain(url) or f.path != "/watch":
        return None
    return f.args.get("v")


def save_video_data(video_id):
    """Save video data to a JSON file"""
    request = youtube.videos().list(  # pylint: disable=no-member
        part="contentDetails, id, liveStreamingDetails, "
        "localizations, paidProductPlacementDetails, player, "
        "recordingDetails, snippet, statistics, status, topicDetails",
        id=video_id,
    )
    response = request.execute()
    with open(f"{video_id}.json", "w", encoding="utf-8") as f:
        json.dump(response, f, ensure_ascii=False, indent=4)

def save_videos_data(video_ids: list[str]):
    """Save video data to a JSON file"""
    PARTITION_LENGTH = 50 # pylint: disable=invalid-name
    partitions = list(partition_all(PARTITION_LENGTH, video_ids))
    for partition in partitions:
        request = youtube.videos().list(  # pylint: disable=no-member
            part="contentDetails, id, liveStreamingDetails, "
            "localizations, paidProductPlacementDetails, player, "
            "recordingDetails, snippet, statistics, status, topicDetails",
            id=ic(list(partition)),
            maxResults=PARTITION_LENGTH,
        )
        videos_data = request.execute().get("items", [])

        for video_data in videos_data:
            video_id = video_data["id"]
            with open(f"video[{video_id}].json", "w", encoding="utf-8") as f:
                json.dump(video_data, f, ensure_ascii=False, indent=4)
