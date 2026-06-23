"""Helpers to build YouTube Data API request specs (URL + params)."""

from __future__ import annotations

from typing import Tuple, Dict, List

YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"


def videos_spec(ids: List[str], api_key: str, parts: str) -> Tuple[str, Dict]:
    url = f"{YOUTUBE_API_BASE}/videos"
    params = {"part": parts, "id": ",".join(ids), "key": api_key}
    return url, params


def playlists_spec(ids: List[str], api_key: str, parts: str) -> Tuple[str, Dict]:
    url = f"{YOUTUBE_API_BASE}/playlists"
    params = {"part": parts, "id": ",".join(ids), "key": api_key}
    return url, params


def channels_spec(ids: List[str], api_key: str, parts: str) -> Tuple[str, Dict]:
    url = f"{YOUTUBE_API_BASE}/channels"
    params = {"part": parts, "id": ",".join(ids), "key": api_key}
    return url, params


def playlistitems_spec(
    playlist_id: str,
    api_key: str,
    parts: str,
    max_results: int = 50,
    page_token: str | None = None,
) -> Tuple[str, Dict]:
    url = f"{YOUTUBE_API_BASE}/playlistItems"
    params = {
        "part": parts,
        "playlistId": playlist_id,
        "maxResults": max_results,
        "key": api_key,
    }
    if page_token:
        params["pageToken"] = page_token
    return url, params


__all__ = ["videos_spec", "playlists_spec", "playlistitems_spec"]
