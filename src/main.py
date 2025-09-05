"""Main application. Save video data to a JSON file"""

import sys
import urllib.request
from typing import Iterator, Iterable
from furl import furl
from icecream import ic  # pylint: disable=unused-import
from kinds.kind import Kind
from kinds.video import Video
from kinds.playlist import Playlist
from properties.data_getter import DataGetter
from properties.resource_id_getter import ResourceIdGetter
from type_aliases import *  # pylint: disable=wildcard-import, unused-wildcard-import
from utils import save_as_jsons


resource_kinds: list[Kind] = [Video(), Playlist(),]


# TODO: fix bug. Does not work properly. Method Kind.get works properly. Example:
# >> process_urls({"https://www.youtube.com/playlist?list=PLmsony4NVQpxYb6B51t-uWWuGkph5rmf1"})
# >> {'https://www.youtube.com/playlist?list=PLmsony4NVQpxYb6B51t-uWWuGkph5rmf1':
#                                 {<kinds.playlist.Playlist object at 0x000001CE4BBAA900>:
#                                  'PLmsony4NVQpxYb6B51t-uWWuGkph5rmf1',
#                                  <kinds.video.Video object at 0x000001CE4BBAA7B0>:
#                                  'PLmsony4NVQpxYb6B51t-uWWuGkph5rmf1'}}
def process_urls(urls: Iterable[URL]) -> Iterator[tuple[Kind, URL, Id | None]]:
    """Get resource type, kind and id for each URL"""
    for kind in resource_kinds:
        ic(resource_kinds)
        ic(kind.get(ResourceIdGetter))
        ic((kind._properties))
        ic(kind.get.__defaults__)
        for url in urls:
            yield (kind, url, kind.get(ResourceIdGetter, ResourceIdGetter())(url))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 save_video_data.py URL1 URL2 ...")
        sys.exit(1)
    data: list[dict] = list()
    ic(Playlist().get(ResourceIdGetter, ResourceIdGetter())("https://www.youtube.com/watch?v=zZVpXjZ9igs"))
    ids: dict[Kind, list[Id]] = dict()
    for kind, url, id in process_urls(sys.argv[1:]):
        print(f"{kind}: {url} -> {id}")
        if id is not None:
            ids[kind] = ids.get(kind, list()) + [id]
    for kind, ids_list in ids.items():
        print("working with:", kind)
        partial_data = kind.get(DataGetter, DataGetter())(ids_list)
        data.extend(partial_data)
        save_as_jsons(partial_data)
    keys_levels = {"default": 1, "medium": 2, "high": 3, "standard": 4, "maxres": 5}
    for item in data:
        keys = item.get("snippet", dict()).get("thumbnails", dict()).keys()
        highest_level = max(map(lambda x: keys_levels[x], keys))
        thumbnail_url = (
            item.get("snippet", dict())
            .get("thumbnails", dict())
            .get(
                dict(zip(keys_levels.values(), keys_levels.keys()))[highest_level],
                dict(),
            )
            .get("url")
        )
        if thumbnail_url is None:
            continue
        print("downloading", thumbnail_url)
        filename = furl(thumbnail_url).path.segments[-1].split(".")
        try:
            urllib.request.urlretrieve(
                thumbnail_url, f"{filename[0]}[{item["id"]}].{filename[1]}"
            )
        except Exception as e:
            print(e)
