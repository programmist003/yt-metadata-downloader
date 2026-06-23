"""Utility helpers used across the project."""

import json
from urllib.request import urlopen
from furl import furl


def clean_url(url: str) -> str:
    """Resolve redirects and return final URL."""
    with urlopen(url) as response:
        return response.geturl()


def check_domain(url: str) -> bool:
    """Return True if URL host belongs to YouTube."""
    host = furl(url).host
    return host in ("youtube.com", "www.youtube.com", "youtu.be")


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
