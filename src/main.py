"""Main application. Interactive YouTube URL input and raw API response output."""

from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

from furl import furl
from auth import load_api_key
from kinds.video import get_video_id
from kinds.playlist import get_playlist_id
from type_aliases import *  # pylint: disable=wildcard-import, unused-wildcard-import


YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"
VIDEO_PARTS = "contentDetails,id,liveStreamingDetails,localizations,paidProductPlacementDetails,player,recordingDetails,snippet,statistics,status,topicDetails"
PLAYLIST_PARTS = "contentDetails,id,localizations,player,snippet,status"
PLAYLIST_ITEMS_PARTS = "contentDetails,id,snippet,status"
MAX_RESULTS = 50
RETRY_COUNT = 2
RETRY_DELAY = 1


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


def get_resource_kind_and_id(url: str) -> tuple[Optional[str], Optional[Id]]:
    """Detect resource kind and return (`video`|`playlist`, id) or (None, None)."""
    v = get_video_id(url)
    if v:
        return "video", v
    p = get_playlist_id(url)
    if p:
        return "playlist", p
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
    kind, _ = get_resource_kind_and_id(url)
    return kind is not None


def is_playlist_url(url: str) -> bool:
    kind, _ = get_resource_kind_and_id(url)
    return kind == "playlist"


def http_get_json(url: str) -> Optional[dict]:
    req = urllib.request.Request(
        url, headers={"User-Agent": "yt-metadata-downloader/1.0"}
    )
    for attempt in range(1, RETRY_COUNT + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as error:
            sys.stderr.write(f"HTTP error for URL {url}: {error.code} {error.reason}")
            sys.stderr.write("\n")
            sys.stderr.flush()
            if attempt < RETRY_COUNT and 500 <= error.code < 600:
                time.sleep(RETRY_DELAY)
                sys.stderr.write(f"Retrying ({attempt + 1}/{RETRY_COUNT})...\n")
                sys.stderr.flush()
                continue
            return None
        except urllib.error.URLError as error:
            sys.stderr.write(f"URL error for URL {url}: {error}\n")
            sys.stderr.flush()
            if attempt < RETRY_COUNT:
                time.sleep(RETRY_DELAY)
                sys.stderr.write(f"Retrying ({attempt + 1}/{RETRY_COUNT})...\n")
                sys.stderr.flush()
                continue
            return None
        except Exception as error:
            sys.stderr.write(f"Request failed for URL {url}: {error}\n")
            sys.stderr.flush()
            if attempt < RETRY_COUNT:
                time.sleep(RETRY_DELAY)
                sys.stderr.write(f"Retrying ({attempt + 1}/{RETRY_COUNT})...\n")
                sys.stderr.flush()
                continue
            return None
    return None


def fetch_videos(ids: list[Id], api_key: str) -> list[dict]:
    items: list[dict] = []
    for i in range(0, len(ids), MAX_RESULTS):
        chunk = ids[i : i + MAX_RESULTS]
        q = urllib.parse.urlencode(
            {"part": VIDEO_PARTS, "id": ",".join(chunk), "key": api_key}
        )
        url = f"{YOUTUBE_API_BASE}/videos?{q}"
        data = http_get_json(url)
        if data is None:
            continue
        items.extend(data.get("items", []))
    return items


def fetch_playlists(ids: list[Id], api_key: str) -> list[dict]:
    items: list[dict] = []
    for i in range(0, len(ids), MAX_RESULTS):
        chunk = ids[i : i + MAX_RESULTS]
        q = urllib.parse.urlencode(
            {"part": PLAYLIST_PARTS, "id": ",".join(chunk), "key": api_key}
        )
        url = f"{YOUTUBE_API_BASE}/playlists?{q}"
        data = http_get_json(url)
        if data is None:
            continue
        items.extend(data.get("items", []))
    return items


def fetch_playlist_items(ids: list[Id], api_key: str) -> list[dict]:
    items: list[dict] = []
    for pid in ids:
        page_token: Optional[str] = None
        while True:
            qd = {
                "part": PLAYLIST_ITEMS_PARTS,
                "playlistId": pid,
                "maxResults": MAX_RESULTS,
                "key": api_key,
            }
            if page_token:
                qd["pageToken"] = page_token
            q = urllib.parse.urlencode(qd)
            url = f"{YOUTUBE_API_BASE}/playlistItems?{q}"
            data = http_get_json(url)
            if data is None:
                sys.stderr.write(f"Failed to fetch playlist items for playlist {pid}\n")
                sys.stderr.flush()
                break
            items.extend(data.get("items", []))
            page_token = data.get("nextPageToken")
            if not page_token:
                break
    return items


def fetch_raw_responses(urls: list[URL], api_key: str) -> list[dict]:
    vids: list[Id] = []
    pls: list[Id] = []
    for url in urls:
        kind, rid = get_resource_kind_and_id(url)
        if kind == "video" and rid:
            vids.append(rid)
        elif kind == "playlist" and rid:
            pls.append(rid)

    responses: list[dict] = []
    if vids:
        try:
            responses.extend(fetch_videos(vids, api_key))
        except Exception as e:
            sys.stderr.write(f"API request failed for videos: {e}\n")
            sys.stderr.flush()
    if pls:
        try:
            responses.extend(fetch_playlists(pls, api_key))
        except Exception as e:
            sys.stderr.write(f"API request failed for playlists: {e}\n")
            sys.stderr.flush()
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
    raw.extend(fetch_raw_responses(first_block, api_key))

    # fetch playlistItems for second block
    playlist_ids = [get_playlist_id(u) for u in second_block]
    playlist_ids = [p for p in playlist_ids if p]
    try:
        raw.extend(fetch_playlist_items(playlist_ids, api_key))
    except Exception as e:
        sys.stderr.write(f"API request failed for playlistItems: {e}\n")
        sys.stderr.flush()

    # Write UTF-8 bytes to avoid console encoding issues on Windows
    output = json.dumps(raw, ensure_ascii=False, indent=2)
    sys.stdout.buffer.write(output.encode("utf-8"))
    sys.stdout.buffer.write(b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
