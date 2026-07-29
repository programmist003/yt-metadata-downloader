from typing import Union
from .url import URL


def cast_to_URL(url: Union[str, URL]) -> URL:
    """Cast a URL string or URL object to a URL object."""
    if isinstance(url, URL):
        return url
    return URL.parse(url)
