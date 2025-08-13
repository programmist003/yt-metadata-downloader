"""Main application. Save video data to a JSON file"""

import sys
from icecream import ic
from kinds.video import get_video_id
from kinds.video import save_video_data


resource_kinds = {}


def get_resource_type(url: str) -> tuple[str | None, str | None]:
    """Returns type of resource and its id"""
    types = {
        "watch": ("video", lambda x: x.split("=")[-1]),
        "playlist": ("playlist", lambda x: x.split("=")[-1]),
        "post": ("post", lambda x: x.split("/")[-1]),
    }
    for type, func in types.items(): # pylint: disable=redefined-builtin
        if type in url:
            return func[0], func[1](url)
    return None, None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 save_video_data.py URL1 URL2 ...")
        sys.exit(1)
    video_ids = [get_video_id(link) for link in sys.argv[1:]]
    for video_id in video_ids:
        ic(video_id)
        save_video_data(video_id)
