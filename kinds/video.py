"""YouTube video resource kind module"""

from furl import furl
from kinds.kind import Kind
from properties.resource_id_getter import ResourceIdGetter
from urlparse import check_domain



class Video(Kind):
    """YouTube video resource kind"""
    def __init__(self, *properties: list):
        self.add(ResourceIdGetter(get_video_id))
        super().__init__(*properties)

def get_video_id(url: str) -> str | None:
    """Get video ID from a YouTube URL"""
    f = furl(url)
    if not check_domain(url) or f.path != "/watch":
        return None
    return f.args.get("v")