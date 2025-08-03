import sys
import json
from googleapiclient.discovery import build
import toml
from icecream import ic


DEVELOPER_KEY = toml.load("config.toml")["api_key"]
# API client
youtube = build("youtube", "v3", developerKey=DEVELOPER_KEY)
# https://developers.google.com/youtube/v3/docs/videos/list


def get_video_id(url):
    """Get video ID from a YouTube URL"""
    return url.split("=")[-1]


def save_video_data(video_id):
    """Save video data to a JSON file"""
    request = youtube.videos().list(
        part="contentDetails, id, liveStreamingDetails, localizations, paidProductPlacementDetails, player, recordingDetails, snippet, statistics, status, topicDetails",
        id=video_id,
    )
    response = request.execute()
    with open(f"{video_id}.json", "w", encoding="utf-8") as f:
        json.dump(response, f, ensure_ascii=False, indent=4)

def get_resource_type(url: str) -> tuple[str|None, str|None]:
    """Returns type of resource and its id"""
    types = {
        "watch": ("video", lambda x: x.split("=")[-1]),
        "playlist": ("playlist", lambda x: x.split("=")[-1]),
        "post": ("post", lambda x: x.split("/")[-1])
    }
    for type, func in types.items():
        if type in url:
            return func[0], func[1](url)
    return None, None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 save_video_data.py URL")
        sys.exit(1)
    video_ids = [get_video_id(link) for link in sys.argv[1:]]
    for video_id in video_ids:
        if get_resource_type(video_id)[0] != "video":
            continue
        ic(video_id)
        save_video_data(video_id)