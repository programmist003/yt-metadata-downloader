"""Data getter module"""

from typing import Callable, NamedTuple

DataGetterFunction = Callable[[list[str]], None]


class DataGetter(NamedTuple):
    """Data getter"""

    data_getter: DataGetterFunction

    def __call__(self, resource_id: list[str]) -> None:
        return self.data_getter(resource_id)
