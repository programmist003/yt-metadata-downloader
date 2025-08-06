"""Resource kind base class module"""
from typing import Self

class Kind:
    """Resource kind base class"""

    _properties: dict[type, object]

    def __init__(self, *properties: list):
        """Initialize the kind"""
        self.add(*properties)

    def add(self, *properties) -> Self:
        """Add a component to the kind"""
        self._properties.update({type(prop): prop for prop in properties})
        return self

    def get(self, property_type: type) -> object:
        """Get a component from the kind"""
        return self._properties[property_type]

    def delete(self, property_type: type) -> None:
        """Delete a component from the kind"""
        del self._properties[property_type]
