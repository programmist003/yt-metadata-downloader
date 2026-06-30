"""Configuration module for YouTube Metadata Downloader."""

from __future__ import annotations

# YouTube API parts for different resource types
VIDEO_PARTS = (
    "contentDetails,id,liveStreamingDetails,localizations,paidProductPlacementDetails,"
    "player,recordingDetails,snippet,statistics,status,topicDetails"
)
PLAYLIST_PARTS = "contentDetails,id,localizations,player,snippet,status"
PLAYLIST_ITEMS_PARTS = "contentDetails,id,snippet,status"

# Maximum number of results per API request
MAX_RESULTS = 50

# YouTube API base URL
YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"

# HTTP client settings
HTTP_RETRIES = 3
HTTP_BACKOFF = 1.0
HTTP_TIMEOUT = 30

# User agent for HTTP requests
USER_AGENT = "yt-metadata-downloader/1.0"

__all__ = [
    "VIDEO_PARTS",
    "PLAYLIST_PARTS",
    "PLAYLIST_ITEMS_PARTS",
    "MAX_RESULTS",
    "YOUTUBE_API_BASE",
    "HTTP_RETRIES",
    "HTTP_BACKOFF",
    "HTTP_TIMEOUT",
    "USER_AGENT",
]