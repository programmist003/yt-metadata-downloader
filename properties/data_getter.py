"""Data getter module"""

from typing import Any, Callable, NamedTuple

Id = str
DataGetterFunction = Callable[[Id], None]


class DataGetter(NamedTuple):
    """Data getter"""

    data_getter: DataGetterFunction

    def __call__(self, resource_id: Id) -> Any:
        return self.data_getter(resource_id)
