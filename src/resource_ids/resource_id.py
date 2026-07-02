"""Resource identifiers for different types of YouTube resources."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Union

from query_makers import QueryMaker


class ResourceId(ABC):
    """Abstract base class for resource identifiers."""

    value: str
    kind: str
    query_maker: QueryMaker

    @classmethod
    @abstractmethod
    def from_urls(cls, urls: List[str]) -> List[Union[ResourceId, None]]:
        """Create a list of ResourceId from a list of URLs."""


@dataclass
class ResourceIdBase(ResourceId):
    """Base class for resource identifiers."""

    value: str
    kind: str
    query_maker: QueryMaker

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ResourceId):
            return False
        return self.value == other.value and self.kind == other.kind

    def to_dict(self) -> Dict[str, str]:
        """Convert the resource ID to a dictionary."""
        return {
            "value": self.value,
            "kind": self.kind,
        }


__all__ = [
    "ResourceIdBase",
    "ResourceId",
]
