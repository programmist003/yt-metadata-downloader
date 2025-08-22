"""Main application. Save video data to a JSON file"""

import sys
import pandas as pd
from icecream import ic # pylint: disable=unused-import
from kinds.kind import Kind
from kinds.video import Video
from properties.data_getter import DataGetter
from properties.resource_id_getter import ResourceIdGetter
from type_aliases import *  # pylint: disable=wildcard-import, unused-wildcard-import
from utils import save_as_jsons
from auth import youtube


resource_kinds: list[Kind] = [Video()]


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
        partial_data = kind.get(DataGetter, lambda x: None)(  # type: ignore
            list(filter(lambda x: x is not None, set(ids.values)))
        )
        data.extend(partial_data)
        save_as_jsons(partial_data)
    category_ids = set()
    for item in data:
        category_ids.add(item.get("snippet", dict()).get("categoryId"))
    category_data = youtube.videoCategories().list(  # type: ignore # pylint: disable=no-member
        part="id, snippet",
        id=list(filter(lambda x: x is not None, category_ids)),
    ).execute().get("items", list())
    save_as_jsons(category_data)
