"""Base query maker for YouTube API requests."""

from __future__ import annotations

from typing import Dict, List, Tuple


class QueryMaker:
    """Base class for creating YouTube API queries."""

    def __init__(self, parts: str):
        self.parts = parts

    def make_query(
        self, resource_ids: List[str], api_key: str, max_results: int = 50
    ) -> Tuple[str, Dict]:
        """Create a query for the given resource IDs."""
        raise NotImplementedError("This method should be implemented by subclasses.")