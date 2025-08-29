"""YouTube playlist resource kind module"""

from icecream import ic  # pylint: disable=unused-import
from furl import furl
from kinds.kind import Kind
from properties.data_getter import DataGetter
from properties.resource_id_getter import ResourceIdGetter
from utils import check_domain, prepare_list_method_method
from auth import youtube


def get_playlist_id(url: str) -> str | None:
    """Get playlist ID from a YouTube URL"""
    f = furl(url)
    if not check_domain(url) or f.path != "/playlist":
        return None
    return f.args.get("list")


class Playlist(Kind):
    """YouTube playlist resource kind"""

    def __init__(self, *properties: list):
        self.add(ResourceIdGetter(get_playlist_id))
        self.add(
            DataGetter(
                prepare_list_method_method(
                    youtube.playlists(),  # type: ignore # pylint: disable=no-member
                    "contentDetails, id, localizations, player, snippet, status",
                )
            )
        )
        super().__init__(*properties)
