"""Resolve YouTube resource identifiers to canonical IDs.

Primary task: resolve channel handles and custom names to `channelId` using
YouTube Data API `channels` endpoint with `forHandle` and `forUsername`.

This module intentionally avoids search and scraping; if resolution via API
fails, `None` is returned.
"""

from __future__ import annotations

from typing import Optional, Dict
import sys

import requests

from links.parser import parse_url


YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"


def resolve_channel_id(
    parsed: Dict[str, Optional[str]], api_key: str, timeout: int = 30
) -> Optional[str]:
    """Resolve a parsed URL dict (from `parse_url`) to a `channelId`.

    Returns `channelId` string on success or `None` when not resolvable.
    """
    if not parsed:
        return None

    t = parsed.get("type")
    ident = parsed.get("identifier")

    # If it's already a channel ID, return it directly
    if t == "channel_id":
        return ident

    params = {"part": "id", "key": api_key}

    if t == "channel_handle":
        if not ident:
            return None
        # API accepts handle with or without '@'; send without leading @ for consistency
        handle = ident[1:] if ident.startswith("@") else ident
        params["forHandle"] = handle
    elif t == "channel_custom":
        if not ident:
            return None
        params["forUsername"] = ident
    else:
        return None

    url = f"{YOUTUBE_API_BASE}/channels"
    headers = {"User-Agent": "yt-metadata-downloader/1.0"}

    try:
        resp = requests.get(url, params=params, timeout=timeout, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("items", [])
        if not items:
            return None
        # items[0].get('id') is the channelId
        return items[0].get("id")
    except requests.RequestException as e:
        sys.stderr.write(f"Failed to resolve channel id for {parsed!r}: {e}\n")
        sys.stderr.flush()
        return None


def resolve_channel_id_from_url(
    url: str, api_key: str, timeout: int = 30
) -> Optional[str]:
    parsed = parse_url(url)
    return resolve_channel_id(parsed, api_key, timeout=timeout)


__all__ = ["resolve_channel_id", "resolve_channel_id_from_url"]
