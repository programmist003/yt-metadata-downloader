"""Base query maker for YouTube API requests."""

from __future__ import annotations

from typing import Dict, List, Tuple, TypeVar

from config import MAX_RESULTS

from resource_ids.resource_id import ResourceId

T = TypeVar("T", bound=ResourceId)


class QueryMaker:
    """Base class for creating YouTube API queries."""

    def __init__(self, parts: str):
        self.parts = parts

    def make_query(
        self, resource_ids: List[T], api_key: str, max_results: int = MAX_RESULTS
    ) -> Tuple[str, Dict]:
        """Create a query for the given resource IDs."""
        raise NotImplementedError("This method should be implemented by subclasses.")
