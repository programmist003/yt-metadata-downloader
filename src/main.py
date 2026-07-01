"""Main application. Interactive YouTube URL input and raw API response output."""

from __future__ import annotations

import json
import sys
from typing import Optional

from furl import furl

from auth import load_api_key
from config import (
    PLAYLIST_ITEMS_PARTS,
    MAX_RESULTS,
    YOUTUBE_API_BASE,
)
from error_handler import handle_errors, log_error
from type_aliases import *  # pylint: disable=wildcard-import, unused-wildcard-import

from http_client import HttpClient
from resource_ids.video_id import VideoId
from resource_ids.playlist_id import PlaylistId
from resource_ids.channel_id import ChannelId


def prompt_stderr(message: str) -> Optional[str]:
    """Write a prompt to stderr and read a line from stdin."""
    sys.stderr.write(message)
    sys.stderr.flush()
    line = sys.stdin.readline()
    if line == "":
        return None
    return line.rstrip("\n")


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
        playlist_id = PlaylistId.from_urls([u])[0]
        if playlist_id is not None:
            playlist_ids.append(playlist_id)
    raw.extend(fetch_playlist_items(playlist_ids, api_key) or [])

    # Write UTF-8 bytes to avoid console encoding issues on Windows
    output = json.dumps(raw, ensure_ascii=False, indent=2)
    sys.stdout.buffer.write(output.encode("utf-8"))
    sys.stdout.buffer.write(b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
