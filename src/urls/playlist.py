from dataclasses import dataclass
from typing import Literal, Optional, Tuple, TypedDict, Union

from .utils import cast_to_URL
from .validated_url import ValidatedURL
from .url import URL


class StandartQueryDict(TypedDict):
    list: Tuple[str]


@dataclass
class Standart(ValidatedURL):
    scheme: str
    host: Literal["youtube.com", "www.youtube.com"]
    path: Tuple[Literal["playlist"]]
    port: Optional[int]
    query: StandartQueryDict
    fragment: Optional[str] = None

    @classmethod
    def parse(cls, url: Union[str, URL]) -> Optional["Standart"]:
        url = cast_to_URL(url)
        if (
            url.host in ("youtube.com", "www.youtube.com")
            and url.query is not None
            and len(url.query.get("list", tuple())) == 1
            and url.path[0] == "playlist"
            and len(url.path) == 1
        ):
            return Standart(
                scheme=url.scheme,
                host=url.host,
                port=url.port,
                path=(url.path[0],),
                query={"list": (url.query["list"][-1],)},
                fragment=url.fragment,
            )
