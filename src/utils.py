"""Utility helpers used across the project."""

import json
from typing import Dict, List
from urllib.request import urlopen
from furl import furl

from urls.url import URL
from type_vars import K, V

def normalize_dict(listed_dict: Dict[K, List[V]]):
    return {k: v[-1] for k, v in listed_dict.items()}

def clean_url(url: str) -> str:
    """Resolve redirects and return final URL."""
    with urlopen(url) as response:
        return response.geturl()


def check_domain(url: URL) -> bool:
    """Return True if URL host belongs to YouTube."""
    return url.host in ("youtube.com", "www.youtube.com", "youtu.be")


def save_as_jsons(resources_data: list[dict]) -> None:
    """Save list of resource dicts as individual JSON files."""
    for resource_data in resources_data:
        resource_id = resource_data.get("id")
        kind = resource_data.get("kind")
        if not resource_id or not kind:
            continue
        resource_kind = kind.split("#")[-1]
        with open(f"{resource_kind}[{resource_id}].json", "w", encoding="utf-8") as f:
            json.dump(resource_data, f, ensure_ascii=False, indent=4)


def is_youtube_url(url: URL) -> bool:
    """Check if the host is a YouTube domain.

    Args:
        url: URL object to check.

    Returns:
        bool: True if the URL belongs to YouTube, False otherwise.
    """
    youtube_domains = (
        "youtube.com",
        "www.youtube.com",
        "youtu.be",
        "m.youtube.com",
        "music.youtube.com",
        "gaming.youtube.com",
    )
    return any(domain in url.host for domain in youtube_domains)


__all__ = ["clean_url", "check_domain", "save_as_jsons", "is_youtube_url"]
