"""URL parser module"""

from urllib.request import urlopen
from typing import Callable
from googleapiclient.discovery import Resource
from toolz import partition_all
from furl import furl
from type_aliases import Id


def clean_url(url: str):
    """Clears URLs form redirects"""
    with urlopen(url) as response:
        url = response.geturl()
    return url


def check_domain(url: str) -> bool:
    """Check if the URL is a YouTube URL"""
    host = furl(url).host
    return host in ("youtube.com", "www.youtube.com", "youtu.be")


def prepare_list_method_method(resource: Resource, parts: str)->Callable[[list[Id]], list[dict]]:
    """Prepare a list method for a resource kind"""

    def wrapper(ids: list[Id]):
        PARTITION_LENGTH = 50  # pylint: disable=invalid-name
        partitions = list(partition_all(PARTITION_LENGTH, ids))
        videos_data: list = []
        for partition in partitions:
            request = resource.list(  # type: ignore
                part=parts,
                id=partition,
                maxResults=PARTITION_LENGTH,
            )
            videos_data.append(request.execute().get("items", []))
        return videos_data

    return wrapper
