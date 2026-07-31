from dataclasses import dataclass
from typing import Literal, Optional, Tuple, Union
from typing_extensions import Annotated

from ..utils import cast_to_URL
from ..validated_url import ValidatedURL
from ..url import URL


@dataclass
class Id(ValidatedURL):
    scheme: str
    host: Literal["youtube.com", "www.youtube.com"]
    path: Tuple[Literal["channel"], str]
    port: Optional[int] = None
    query: None = None
    fragment: Optional[str] = None

    @classmethod
    def parse(cls, url: Union[str, URL]) -> Optional["Id"]:
        url = cast_to_URL(url)
        if (
            url.host in ("youtube.com", "www.youtube.com")
            and url.query is None
            and len(url.path) == 2
            and url.path[0] == "channel"
        ):
            return Id(
                scheme=url.scheme,
                host=url.host,
                port=url.port,
                path=(url.path[0], url.path[1]),
                query=url.query,
                fragment=url.fragment,
            )