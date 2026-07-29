from typing import Callable, Optional, Iterable

from urls.url import URL


def parse_by_parsers(
    url: URL, parsers: Iterable[Callable[[URL], Optional[str]]]
) -> Optional[str]:
    for parser in parsers:
        result = parser(url)
        if result:
            return result
    return None
