"""Main application. Interactive YouTube URL input and raw API response output."""

from __future__ import annotations

import json
import sys
from typing import Optional

from furl import furl
from auth import load_api_key, set_api_key
from kinds.kind import Kind
from kinds.playlist import Playlist
from kinds.video import Video
from properties.data_getter import DataGetter
from properties.resource_id_getter import ResourceIdGetter
from type_aliases import *  # pylint: disable=wildcard-import, unused-wildcard-import


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


def get_resource_kind_and_id(
    url: str, kinds: list[Kind]
) -> tuple[Optional[Kind], Optional[Id]]:
    """Find the first supported kind for a URL and extract its resource ID."""
    for kind in kinds:
        resource_id = kind.get(ResourceIdGetter, ResourceIdGetter())(url)
        if resource_id is not None:
            return kind, resource_id
    return None, None


def collect_urls(
    prompt_title: str,
    validation: callable,
    kinds: list[Kind],
    seen: set[str] | None = None,
) -> list[URL]:
    """Collect a list of validated unique URLs from stdin."""
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


def is_supported_resource_url(url: str, kinds: list[Kind]) -> bool:
    """Check whether URL is supported by any available kind."""
    kind, _ = get_resource_kind_and_id(url, kinds)
    return kind is not None


def is_playlist_url(url: str) -> bool:
    """Check whether URL is a playlist URL."""
    playlist_kind = Playlist()
    _, resource_id = get_resource_kind_and_id(url, [playlist_kind])
    return resource_id is not None


def fetch_raw_responses(urls: list[URL], kinds: list[Kind]) -> list[dict]:
    """Query YouTube API for each supported kind and return raw item responses."""
    ids_by_kind: dict[Kind, list[Id]] = {}
    for url in urls:
        kind, resource_id = get_resource_kind_and_id(url, kinds)
        if kind is None or resource_id is None:
            continue
        ids_by_kind.setdefault(kind, []).append(resource_id)

    responses: list[dict] = []
    for kind, ids in ids_by_kind.items():
        try:
            data_getter = kind.get(DataGetter, DataGetter())
            responses.extend(data_getter(ids))
        except Exception as error:
            sys.stderr.write(f"API request failed for {kind}: {error}\n")
            sys.stderr.flush()
    return responses


def main() -> int:
    """Run interactive input, fetch YouTube data, and print JSON responses."""
    api_key = prompt_stderr(
        "Enter YouTube API key [press Enter to use config.toml]: ",
    )
    if api_key is None:
        sys.stderr.write("EOF received while reading API key.\n")
        sys.stderr.flush()

    try:
        if api_key:
            set_api_key(api_key)
        else:
            config_key = load_api_key()
            if not config_key:
                sys.stderr.write(
                    "YouTube API key was not provided and config.toml does not contain api_key.\n"
                )
                sys.stderr.flush()
                return 1
    except Exception as error:
        sys.stderr.write(f"Failed to initialize API key: {error}\n")
        sys.stderr.flush()
        return 1

    resource_kinds: list[Kind] = [Video(), Playlist()]
    seen_urls: set[str] = set()

    first_block_urls = collect_urls(
        "Enter supported resource URLs (video or playlist).",
        lambda url: is_supported_resource_url(url, resource_kinds),
        resource_kinds,
        seen=seen_urls,
    )

    second_block_urls = collect_urls(
        "Enter playlist URLs for PlaylistItems.",
        is_playlist_url,
        resource_kinds,
        seen=seen_urls,
    )

    if second_block_urls and not first_block_urls:
        sys.stderr.write(
            "Playlist items section is filled, resource section was empty.\n"
        )
        sys.stderr.flush()

    raw_responses: list[dict] = []
    raw_responses.extend(fetch_raw_responses(first_block_urls, resource_kinds))
    raw_responses.extend(fetch_raw_responses(second_block_urls, [Playlist()]))

    json.dump(raw_responses, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
