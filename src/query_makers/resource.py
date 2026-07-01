"""Resource query maker for YouTube API requests."""

from __future__ import annotations

from typing import Dict, List, Tuple

from config import YOUTUBE_API_BASE

from .base import QueryMaker


class ResourceQueryMaker(QueryMaker):
    """Query maker for resource resources."""

    def __init__(self, resource_type: str, parts: str):
        super().__init__(parts)
        self.resource_type = resource_type

    def make_query(
        self, resource_ids: List[str], api_key: str, max_results: int = 50
    ) -> Tuple[str, Dict]:
        """Create a query for the given resource IDs."""
        url = f"{YOUTUBE_API_BASE}/{self.resource_type}"
        params = {
            "part": self.parts,
            "id": ",".join(resource_ids),
            "key": api_key,
            "maxResults": max_results,
        }
        return url, params