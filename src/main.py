"""Main application. Interactive YouTube URL input and raw API response output."""

from __future__ import annotations

import json
import sys
from typing import Optional

from furl import furl

from auth import load_api_key
from config import (
    VIDEO_PARTS,
    PLAYLIST_PARTS,
    PLAYLIST_ITEMS_PARTS,
    MAX_RESULTS,
    USER_AGENT,
    YOUTUBE_API_BASE,
)
from error_handler import handle_errors, log_error
from links.parser import parse_url, get_resource_id
from type_aliases import *  # pylint: disable=wildcard-import, unused-wildcard-import

from http_client import HttpClient
from resource_id import VideoId, PlaylistId, ChannelId


def prompt_stderr(message: str) -> Optional[str]:
    """Write a prompt to stderr and read a line from stdin."""
    sys.stderr.write(message)
    sys.stderr.flush()
    line = sys.stdin.readline()
    if line == "":
        return None
    return line.rstrip("\n")


def is_valid_url(url: str) -> bool:
    """Validate basic URL syntax."""
    try:
        parsed = furl(url)
    except ValueError:
        return False
    return bool(parsed.scheme) and bool(parsed.host)


def get_resource_kind_and_id(url: str) -> tuple[Optional[str], Optional[str]]:
    """Detect resource kind and return (`video`|`playlist`|`channel`, id) or (None, None).

    Uses `get_resource_id` from `src.links.parser` to extract the identifier.
    """
    resource_id = get_resource_id(url)
    if resource_id:
        if isinstance(resource_id, VideoId):
            return "video", resource_id.value
        elif isinstance(resource_id, PlaylistId):
            return "playlist", resource_id.value
        elif isinstance(resource_id, ChannelId):
            return "channel", resource_id.value

    return None, None


def collect_urls(
    prompt_title: str, validation: callable, seen: set[str] | None = None
) -> list[URL]:
    """Collect validated unique URLs from stdin; prompts on stderr."""
    urls: list[URL] = []
    if seen is None:
        seen = set()

    sys.stderr.write(f"{prompt_title}\n")
    sys.stderr.write("Enter one URL per line. Press ENTER on empty line to finish.\n")
    sys.stderr.flush()

    while True:
        line = prompt_stderr("URL: ")
        if line is None:
            sys.stderr.write("EOF received, finishing this section.\n")
            sys.stderr.flush()
            break
        if line == "":
            break

        url = line.strip()
        if not url:
            break

        if url in seen:
            sys.stderr.write(f"Duplicate URL ignored: {url}\n")
            sys.stderr.flush()
            continue

        if not is_valid_url(url):
            sys.stderr.write(f"Invalid URL ignored: {url}\n")
            sys.stderr.flush()
            continue

        if not validation(url):
            sys.stderr.write(f"Unsupported URL ignored: {url}\n")
            sys.stderr.flush()
            continue

        urls.append(url)
        seen.add(url)

    return urls


def is_supported_resource_url(url: str) -> bool:
    resource_id = get_resource_id(url)
    return resource_id is not None


def is_playlist_url(url: str) -> bool:
    resource_id = get_resource_id(url)
    return isinstance(resource_id, PlaylistId)


@handle_errors
def fetch_videos(ids: list[VideoId], api_key: str) -> list[dict]:
    responses: list[dict] = []
    client = HttpClient()
    max_results = MAX_RESULTS["video"]
    for i in range(0, len(ids), max_results):
        chunk = [id.value for id in ids[i : i + max_results]]
        url, params = ids[0].query_maker.make_query(chunk, api_key)
        data = client.get_json(url, params=params)
        if data is not None:
            responses.append(data)
    return responses


@handle_errors
def fetch_channels(ids: list[ChannelId], api_key: str) -> list[dict]:
    responses: list[dict] = []
    client = HttpClient()
    max_results = MAX_RESULTS["channel"]
    for i in range(0, len(ids), max_results):
        chunk = [id.value for id in ids[i : i + max_results]]
        url, params = ids[0].query_maker.make_query(chunk, api_key)
        data = client.get_json(url, params=params)
        if data is not None:
            responses.append(data)
    return responses


@handle_errors
def fetch_playlists(ids: list[PlaylistId], api_key: str) -> list[dict]:
    responses: list[dict] = []
    client = HttpClient()
    max_results = MAX_RESULTS["playlist"]
    for i in range(0, len(ids), max_results):
        chunk = [id.value for id in ids[i : i + max_results]]
        url, params = ids[0].query_maker.make_query(chunk, api_key)
        data = client.get_json(url, params=params)
        if data is not None:
            responses.append(data)
    return responses


@handle_errors
def fetch_playlist_items(ids: list[PlaylistId], api_key: str) -> list[dict]:
    responses: list[dict] = []
    client = HttpClient()
    for playlist_id in ids:
        page_token: Optional[str] = None
        while True:
            # Create a query for playlist items using the playlist ID
            url = f"{YOUTUBE_API_BASE}/playlistItems"
            params = {
                "part": PLAYLIST_ITEMS_PARTS,
                "playlistId": playlist_id.value,
                "key": api_key,
                "maxResults": MAX_RESULTS,
                "pageToken": page_token,
            }
            data = client.get_json(url, params=params)
            if data is None:
                log_error(f"Failed to fetch playlist items for playlist {playlist_id}")
                break
            responses.append(data)
            page_token = data.get("nextPageToken")
            if not page_token:
                break
    return responses


@handle_errors
def fetch_raw_responses(urls: list[URL], api_key: str) -> list[dict]:
    vids: list[VideoId] = []
    pls: list[PlaylistId] = []
    chans: list[ChannelId] = []

    for url in urls:
        resource_id = get_resource_id(url)
        if resource_id:
            if isinstance(resource_id, VideoId):
                vids.append(resource_id)
            elif isinstance(resource_id, PlaylistId):
                pls.append(resource_id)
            elif isinstance(resource_id, ChannelId):
                chans.append(resource_id)

    responses: list[dict] = []
    if vids:
        responses.extend(fetch_videos(vids, api_key) or [])
    if pls:
        responses.extend(fetch_playlists(pls, api_key) or [])
    if chans:
        responses.extend(fetch_channels(chans, api_key) or [])
    return responses


def main() -> int:
    api_key = prompt_stderr("Enter YouTube API key [press Enter to use config.toml]: ")
    if api_key is None:
        sys.stderr.write("EOF received while reading API key.\n")
        sys.stderr.flush()

    if not api_key:
        api_key = load_api_key()
        if not api_key:
            sys.stderr.write(
                "YouTube API key not provided and not found in config.toml.\n"
            )
            sys.stderr.flush()
            return 1

    seen: set[str] = set()

    first_block = collect_urls(
        "Enter supported resource URLs (video or playlist).",
        is_supported_resource_url,
        seen=seen,
    )
    second_block = collect_urls(
        "Enter playlist URLs for PlaylistItems.", is_playlist_url, seen=seen
    )

    if second_block and not first_block:
        sys.stderr.write("Playlist items provided while resource section empty.\n")
        sys.stderr.flush()

    raw: list[dict] = []
    raw.extend(fetch_raw_responses(first_block, api_key) or [])

    # fetch playlistItems for second block
    playlist_ids = []
    for u in second_block:
        resource_id = get_resource_id(u)
        if isinstance(resource_id, PlaylistId):
            playlist_ids.append(resource_id)
    raw.extend(fetch_playlist_items(playlist_ids, api_key) or [])

    # Write UTF-8 bytes to avoid console encoding issues on Windows
    output = json.dumps(raw, ensure_ascii=False, indent=2)
    sys.stdout.buffer.write(output.encode("utf-8"))
    sys.stdout.buffer.write(b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
