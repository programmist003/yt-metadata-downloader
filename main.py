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


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 save_video_data.py URL")
        sys.exit(1)
    video_id = get_video_id(sys.argv[1])
    ic(video_id)
    save_video_data(video_id)
