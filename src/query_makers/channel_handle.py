"""Channel handle query maker for YouTube API requests."""

from typing import Dict, List, Tuple

from config import YOUTUBE_API_BASE

from resource_ids.channel_handle import ChannelHandle
from .base import QueryMaker


class ChannelHandleQueryMaker(QueryMaker):
    """Query maker for channel handle resources."""

    def __init__(self, parts: str):
        super().__init__(parts)

    def make_query(
        self, resource_ids: List[ChannelHandle], api_key: str, max_results: int = 50
    ) -> Tuple[str, Dict]:
        """Create a query for the given channel handles."""
        valid_ids = self._filter_valid_ids(resource_ids)
        if not valid_ids:
            raise ValueError("No valid channel handles provided")

        url = f"{YOUTUBE_API_BASE}/channels"
        params = {
            "part": self.parts,
            "forHandle": ",".join(str(id_.value) for id_ in valid_ids),
            "key": api_key,
            "maxResults": max_results,
        }
        return url, params

    def _filter_valid_ids(self, resource_ids: List[ChannelHandle]) -> List[ChannelHandle]:
        """Filter valid channel handles."""
        return [id_ for id_ in resource_ids if isinstance(id_, ChannelHandle)]