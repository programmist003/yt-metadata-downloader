"""Main application. Save video data to a JSON file"""

import sys
import pandas as pd
from furl import furl
import urllib.request
from icecream import ic  # pylint: disable=unused-import
from kinds.kind import Kind
from kinds.video import Video
from kinds.playlist import Playlist
from properties.data_getter import DataGetter
from properties.resource_id_getter import ResourceIdGetter
from type_aliases import *  # pylint: disable=wildcard-import, unused-wildcard-import
from utils import save_as_jsons


resource_kinds: list[Kind] = [Video(), Playlist()]


def get_resource_type(url: str) -> tuple[str | None, str | None]:
    """Returns type of resource and its id"""
    types = {
        "watch": ("video", lambda x: x.split("=")[-1]),
        "playlist": ("playlist", lambda x: x.split("=")[-1]),
        "post": ("post", lambda x: x.split("/")[-1]),
    }
    for type, func in types.items():  # pylint: disable=redefined-builtin
        if type in url:
            return func[0], func[1](url)
    return None, None


# TODO: fix bug. Does not work properly. Method Kind.get works properly. Example:
# >> get_urls_kinds_and_ids({"https://www.youtube.com/playlist?list=PLmsony4NVQpxYb6B51t-uWWuGkph5rmf1"})
# >> {'https://www.youtube.com/playlist?list=PLmsony4NVQpxYb6B51t-uWWuGkph5rmf1':
#                                 {<kinds.playlist.Playlist object at 0x000001CE4BBAA900>:
#                                  'PLmsony4NVQpxYb6B51t-uWWuGkph5rmf1',
#                                  <kinds.video.Video object at 0x000001CE4BBAA7B0>:
#                                  'PLmsony4NVQpxYb6B51t-uWWuGkph5rmf1'}}
def get_urls_kinds_and_ids(urls: set[URL]) -> dict[URL, dict[Kind, Id | None]]:
    """Get resource type, kind and id for each URL"""
    return {
        url: {
            kind: kind.get(ResourceIdGetter, lambda x: None)(url)
            for kind in resource_kinds
        }
        for url in urls
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 save_video_data.py URL1 URL2 ...")
        sys.exit(1)
    ids = pd.DataFrame(get_urls_kinds_and_ids(set(sys.argv[1:])))
    data: list[dict] = list()
    for kind, ids in ids.iterrows():
        print("working with:", kind)
        partial_data = kind.get(DataGetter, lambda x: None)(  # type: ignore
            list(filter(lambda x: x is not None, set(ids.values)))
        )
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
        urllib.request.urlretrieve(
            thumbnail_url, f"{filename[0]}[{item["id"]}].{filename[1]}"
        )
