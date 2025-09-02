"""Resource ID getter module"""

from typing import NamedTuple
from typing import Callable

ResourceIdGetterFunction = Callable[[str], str | None]


class ResourceIdGetter(NamedTuple):
    """Resource ID getter"""

    get_resource_id: ResourceIdGetterFunction = lambda x: None

    def __call__(self, url: str) -> str | None:
        """Get resource ID from a YouTube URL"""
        return self.get_resource_id(url)
