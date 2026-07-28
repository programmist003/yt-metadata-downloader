"""Resource identifiers for different types of YouTube resources."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Union


class ResourceId(ABC):
    """Abstract base class for resource identifiers."""

    value: str
    kind: str

    @classmethod
    @abstractmethod
    def from_url(cls, url: str) -> Optional[ResourceId]:
        """Create a ResourceId from URL"""


@dataclass
class ResourceIdBase(ResourceId):
    """Base class for resource identifiers."""

    value: str
    kind: str

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
