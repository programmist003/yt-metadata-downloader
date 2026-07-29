from typing import Mapping, Optional, Sequence


class ValidatedURL:
    scheme: str
    host: str
    path: Sequence[str]
    port: Optional[int] = None
    query: Optional[Mapping[str, Sequence[str]]] = None
    fragment: Optional[str] = None
