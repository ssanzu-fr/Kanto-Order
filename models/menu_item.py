"""
MenuItem model.
"""
from dataclasses import dataclass


@dataclass
class MenuItem:
    """A single item on the menu."""
    id: str
    name: str
    price: float
    category: str

    def __repr__(self) -> str:
        return f"MenuItem(id='{self.id}', name='{self.name}', price=₱{self.price}, category='{self.category}')"
