"""Channel custom query maker for YouTube API requests."""

from typing import Dict, List, Tuple

from config import YOUTUBE_API_BASE

from resource_ids.channel_custom import ChannelCustom
from .base import QueryMaker


class ChannelCustomQueryMaker(QueryMaker):
    """Query maker for custom channel resources."""

    def __init__(self, parts: str):
        super().__init__(parts)

    def make_query(
        self, resource_ids: List[ChannelCustom], api_key: str, max_results: int = 50
    ) -> Tuple[str, Dict]:
        """Create a query for the given custom channel identifiers."""
        valid_ids = self._filter_valid_ids(resource_ids)
        if not valid_ids:
            raise ValueError("No valid custom channel identifiers provided")

        url = f"{YOUTUBE_API_BASE}/channels"
        params = {
            "part": self.parts,
            "forUsername": ",".join(str(id_.value) for id_ in valid_ids),
            "key": api_key,
            "maxResults": max_results,
        }
        return url, params

    def _filter_valid_ids(self, resource_ids: List[ChannelCustom]) -> List[ChannelCustom]:
        """Filter valid custom channel identifiers."""
        return [id_ for id_ in resource_ids if isinstance(id_, ChannelCustom)]
