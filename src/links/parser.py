"""URL parser for YouTube resources.

Exports:
- `parse_url(url: str) -> dict` — распознаёт тип ресурса и возвращает словарь
  с ключами: `type`, `raw`, `identifier`.

Типы `type`: 'channel_id', 'channel_custom', 'channel_handle',
'video', 'playlist', 'other'.
"""

from __future__ import annotations

from typing import Optional
from urllib.parse import urlparse, parse_qs
import re


def parse_url(url: str) -> dict:
    """Parse YouTube URL and return resource info.

    Returns dict with:
      - type: one of 'channel_id','channel_custom','channel_handle','video','playlist','other'
      - raw: original URL
      - identifier: extracted id or name (without leading @), or None
    """
    p = urlparse(url)
    host = (p.netloc or "").lower()
    path = p.path or ""
    query = parse_qs(p.query or "")

    def mk(t: str, ident: Optional[str]):
        return {"type": t, "raw": url, "identifier": ident}

    # Accept common youtube hosts
    if not any(h in host for h in ("youtube.com", "youtu.be")):
        return mk("other", None)

    # Short youtu.be links: path is /<videoId>
    if "youtu.be" in host:
        vid = path.lstrip("/")
        return mk("video", vid if vid else None)

    # video by query v= or embed
    if "v" in query and query["v"]:
        return mk("video", query["v"][0])
    m = re.match(r"^/embed/([^/]+)", path)
    if m:
        return mk("video", m.group(1))

    # playlist by list=
    if "list" in query and query["list"]:
        return mk("playlist", query["list"][0])

    # /playlist path with query handled above; continue to channel/video patterns
    # channel by id: /channel/<id>
    m = re.match(r"^/channel/([^/]+)", path)
    if m:
        return mk("channel_id", m.group(1))

    # custom channel: /c/<name> or /user/<name>
    m = re.match(r"^/c/([^/]+)", path)
    if m:
        return mk("channel_custom", m.group(1))
    m = re.match(r"^/user/([^/]+)", path)
    if m:
        return mk("channel_custom", m.group(1))

    # handle: /@handle or segments containing @handle
    m = re.match(r"^/@([^/]+)", path)
    if m:
        return mk("channel_handle", m.group(1))
    m = re.search(r"/@([^/]+)", path)
    if m:
        return mk("channel_handle", m.group(1))

    # Fallback: if path looks like a channel handle without leading @ (rare)
    m = re.match(r"^/([A-Za-z0-9_\-]+)/?$", path)
    if m:
        # ambiguous: could be root page; treat as 'other'
        return mk("other", None)

    return mk("other", None)


def is_video_url(url: str) -> bool:
    return parse_url(url)["type"] == "video"


def is_playlist_url(url: str) -> bool:
    return parse_url(url)["type"] == "playlist"


def get_resource_id(url: str) -> Optional[ResourceId]:
    """Parse URL and return appropriate ResourceId object or None."""
    from resource_id import VideoId, PlaylistId, ChannelId

    parsed = parse_url(url)
    ptype = parsed.get("type")
    ident = parsed.get("identifier")

    if ptype == "video" and ident:
        return VideoId(ident)
    elif ptype == "playlist" and ident:
        return PlaylistId(ident)
    elif ptype in ("channel_id", "channel_custom", "channel_handle") and ident:
        return ChannelId(ident)
    else:
        return None


__all__ = ["parse_url", "is_video_url", "is_playlist_url", "get_resource_id"]
