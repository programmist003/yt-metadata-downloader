"""
YouTube video ID extractor module.

This module provides functions to extract video IDs from various YouTube URL formats,
including short URLs (youtu.be), standard URLs with query parameters, and embed URLs.
"""

from typing import Optional

from urls.video import *  # pylint: disable=wildcard-import

from ..urls.url import URL
from .utils import parse_by_parsers


def short(url: URL) -> Optional[str]:
    """Parse video ID from short YouTube URL (youtu.be)"""
    parsed = Short.parse(url)
    if parsed:
        vid = parsed.path[0]
        return vid


def query(url: URL) -> Optional[str]:
    """Parse video ID from standard YouTube URLs (e.g., youtube.com/watch?v=...)."""
    parsed = Standart.parse(url)
    if parsed:
        query_params = parsed.query
        return query_params["v"][-1]


def embed(url: URL) -> Optional[str]:
    """Parse video ID from YouTube embed URLs (e.g., youtube.com/embed/...)."""
    parsed = Embed.parse(url)
    if parsed:
        return parsed.path[-1]


def parse(url: URL) -> Optional[str]:
    """Parse a YouTube video URL and extract video ID using multiple parsers."""
    return parse_by_parsers(url, [short, embed, query])


if __name__ == "__main__":
    print(
        "https://youtu.be/mtpEUZTdeNY?si=FXUSjGxMjMC3cIyq",
        "->",
        short(URL.parse("https://youtu.be/mtpEUZTdeNY?si=FXUSjGxMjMC3cIyq")),
    )
