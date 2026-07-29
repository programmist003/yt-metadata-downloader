from dataclasses import dataclass
from typing import Literal, Optional, Tuple

from urls.validated_url import ValidatedURL
from ..url import URL


@dataclass
class Short(ValidatedURL):
    scheme: str
    host: Literal["youtu.be"]
    path: Tuple[str]
    port: Optional[int] = None
    query: None = None
    fragment: Optional[str] = None

    @classmethod
    def parse(cls, url_str: str) -> Optional["Short"]:
        url = URL.parse(url_str)
        if url.host == "youtu.be" and url.query is None and len(url.path) == 1:
            return Short(
                scheme=url.scheme,
                host=url.host,
                port=url.port,
                path=tuple(url.path),  # type: ignore
                query=url.query,
                fragment=url.fragment,
            )
