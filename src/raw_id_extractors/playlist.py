from typing import Optional

from urls.playlist import Standart

from ..urls.url import URL


def playlist(url: URL) -> Optional[str]:
    """Parse playlist ID from query parameters."""
    parsed = Standart.parse(url)
    if parsed:
        query_params = parsed.query
        return query_params["list"][0]
