"""Data getter module"""

from typing import Callable, NamedTuple

DataGetterFunction = Callable[[list[str]], list[dict]]


class DataGetter(NamedTuple):
    """Data getter"""

    data_getter: DataGetterFunction = lambda x: list()

    def __call__(self, resource_id: list[str]) -> list[dict]:
        return self.data_getter(resource_id)
