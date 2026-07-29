from dataclasses import dataclass
from typing import Literal, Optional, Tuple, TypedDict

from urls.validated_url import ValidatedURL
from ..url import URL


class StandartQueryDict(TypedDict):
    v: Tuple[str]

@dataclass
class Standart(ValidatedURL):
    scheme: str
    host: Literal["youtube.com", "www.youtube.com"]
    path: Tuple[Literal["watch"]]
    port: Optional[int]
    query: StandartQueryDict
    fragment: Optional[str] = None

    @classmethod
    def parse(cls, url_str: str) -> Optional["Standart"]:
        url = URL.parse(url_str)
        if (
            url.host in ("youtube.com", "www.youtube.com")
            and url.query is not None
            and len(url.query.get("v", tuple())) == 1
            and url.path[0] == "watch"
            and len(url.path) == 1
        ):
            return Standart(
                scheme=url.scheme,
                host=url.host,
                port=url.port,
                path=(url.path[0],),
                query={"v": (url.query["v"][-1],)},
                fragment=url.fragment,
            )
