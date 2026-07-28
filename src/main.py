"""Main application. Interactive YouTube URL input and raw API response output."""

from __future__ import annotations

import json
import sys
from typing import Iterable, Optional, Sequence, Type, Dict, List, Tuple

from furl import furl

from auth import load_api_key
from config import (
    PLAYLIST_ITEMS_PARTS,
    MAX_RESULTS,
    YOUTUBE_API_BASE,
)
from error_handler import handle_errors, log_error
from resource_ids import (
    ResourceId,
    VideoId,
    PlaylistId,
    ChannelId,
    ChannelCustom,
    ChannelHandle,
)

from query_makers import *  # pylint: disable=wildcard-import, unused-wildcard-import
from type_aliases import *  # pylint: disable=wildcard-import, unused-wildcard-import

from http_client import HttpClient

MAIN_QUERY_MAKERS = [
    VideoQueryMaker,
    PlaylistQueryMaker,
    ChannelQueryMaker,
    ChannelCustomQueryMaker,
    ChannelHandleQueryMaker,
    PlaylistItemsQueryMaker,
]

SUPPORTED_IDS: Iterable[Type[ResourceId]] = [
    ResourceId,
    VideoId,
    PlaylistId,
    ChannelId,
    ChannelCustom,
    ChannelHandle,
]


def prompt_stderr(message: str) -> Optional[str]:
    """Write a prompt to stderr and read a line from stdin."""
    sys.stderr.write(message)
    sys.stderr.flush()
    line = sys.stdin.readline()
    if line == "":
        return None
    return line.rstrip("\n")


def get_resource_ids(url: str) -> List[ResourceId]:
    """Determine the type of resource for a given URL."""
    resource_ids = []
    for resource_id in SUPPORTED_IDS:
        resource_ids_ = resource_id.from_urls([url])
        if resource_ids_[0] is not None:
            resource_ids.append(resource_ids_[0])
    return resource_ids

def determine_resource_type(url: str) -> Tuple[Optional[Type[ResourceId]], str]:
    """Determine the type of resource for a given URL."""
    for resource_id in SUPPORTED_IDS:
        resource_ids = resource_id.from_urls([url])
        if resource_ids[0] is not None:
            return resource_id, resource_id.__name__
    return None, "unsupported"


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
            sys.stderr.write(f"Duplicate URL ignored: {url} (duplicated)\n")
            sys.stderr.flush()
            continue

        resource_type, type_name = determine_resource_type(url)
        sys.stderr.write(f"URL type: {type_name}\n")
        sys.stderr.flush()

        urls.append(url)
        seen.add(url)

    return urls


def group_urls_by_resource_type(
    urls: list[str],
) -> Dict[Type[ResourceId], List[List[Tuple[str, ResourceId]]]]:
    """Group URLs by resource type and split into chunks of MAX_RESULTS."""
    grouped_urls: Dict[Type[ResourceId], List[List[Tuple[str, ResourceId]]]] = {}

    for url in urls:
        resource_type, _ = determine_resource_type(url)
        if resource_type is None:
            continue

        resource_ids = resource_type.from_urls([url])
        if resource_ids[0] is None:
            continue

        if resource_type not in grouped_urls:
            grouped_urls[resource_type] = []

        if (
            not grouped_urls[resource_type]
            or len(grouped_urls[resource_type][-1]) >= MAX_RESULTS
        ):
            grouped_urls[resource_type].append([])

        grouped_urls[resource_type][-1].append((url, resource_ids[0]))

    return grouped_urls


def fetch_raw_responses(urls: list[str], api_key: str) -> list[dict]:
    """Fetch raw responses from YouTube API for the given URLs."""

    grouped_urls = group_urls_by_resource_type(urls)
    raw_responses: list[dict] = []
    http_client = HttpClient()

    for resource_type, url_chunks in grouped_urls.items():
        for chunk in url_chunks:
            resource_ids = [resource_id for _, resource_id in chunk]
            query_maker = resource_ids[0].query_maker
            url, params = query_maker.make_query(resource_ids, api_key)

            response = http_client.get_json(url, params)
            if response:
                raw_responses.append(response)

    return raw_responses


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
        None,  # Validation is handled by determine_resource_type
        seen=seen,
    )
    second_block = collect_urls(
        "Enter playlist URLs for PlaylistItems.", None, seen=seen
    )

    if second_block and not first_block:
        sys.stderr.write("Playlist items provided while resource section empty.\n")
        sys.stderr.flush()

    raw: list[dict] = []
    raw.extend(fetch_raw_responses(first_block, api_key) or [])

    # fetch playlistItems for second block
    raw.extend(fetch_raw_responses(second_block, api_key) or [])
    # Write UTF-8 bytes to avoid console encoding issues on Windows
    output = json.dumps(raw, ensure_ascii=False, indent=2)
    sys.stdout.buffer.write(output.encode("utf-8"))
    sys.stdout.buffer.write(b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
