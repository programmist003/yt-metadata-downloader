"""Resource query maker for YouTube API requests."""

from __future__ import annotations

from typing import Dict, List, Tuple, Type, Union, TypeVar

from config import YOUTUBE_API_BASE

from resource_ids.resource_id import ResourceId

from .base import QueryMaker

T = TypeVar("T", bound=ResourceId)


class ResourceQueryMaker(QueryMaker):
    """Query maker for resource resources."""

    def __init__(
        self,
        resource_type: str,
        parts: str,
        valid_id_types: Union[Type[T], Tuple[Type[T], ...]],
    ):
        super().__init__(parts)
        self.resource_type = resource_type
        self.valid_id_types = valid_id_types

    def make_query(
        self, resource_ids: List[T], api_key: str, max_results: int = 50
    ) -> Tuple[str, Dict]:
        """Create a query for the given resource IDs."""
        valid_ids = self._filter_valid_ids(resource_ids)
        if not valid_ids:
            raise ValueError("No valid resource IDs provided")

        url = f"{YOUTUBE_API_BASE}/{self.resource_type}"
        params = {
            "part": self.parts,
            "id": ",".join(str(id_.value) for id_ in valid_ids),
            "key": api_key,
            "maxResults": max_results,
        }
        return url, params

    def _filter_valid_ids(self, resource_ids: List[T]) -> List[T]:
        """Filter valid resource IDs for this QueryMaker."""
        if isinstance(self.valid_id_types, tuple):
            return [id_ for id_ in resource_ids if isinstance(id_, self.valid_id_types)]
        else:
            return [id_ for id_ in resource_ids if isinstance(id_, self.valid_id_types)]
