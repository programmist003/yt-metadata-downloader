from dataclasses import dataclass
from typing import Literal, Optional, Tuple

from urls.validated_url import ValidatedURL
from ..url import URL


@dataclass
class Embed(ValidatedURL):
    scheme: str
    host: Literal["youtube.com", "www.youtube.com"]
    path: Tuple[Literal["embed"], str]
    port: Optional[int] = None
    query: None = None
    fragment: Optional[str] = None

    @classmethod
    def parse(cls, url_str: str) -> Optional["Embed"]:
        url = URL.parse(url_str)
        if (
            url.host in ("youtube.com", "www.youtube.com")
            and url.query is None
            and url.path[0] == "embed"
            and isinstance(url.path[1], str)
            and len(url.path) == 2
        ):
            return Embed(
                scheme=url.scheme,
                host=url.host,
                port=url.port,
                path=(url.path[0], url.path[1]),
                query=url.query,
                fragment=url.fragment,
            )
