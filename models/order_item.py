"""
OrderItem model - a menu item with quantity.
"""
from dataclasses import dataclass
from models.menu_item import MenuItem


@dataclass
class OrderItem:
    """A menu item with quantity in an order."""
    menu_item: MenuItem
    quantity: int

    @property
    def subtotal(self) -> float:
        """Calculate subtotal for this item."""
        return self.menu_item.price * self.quantity

    def __repr__(self) -> str:
        return f"OrderItem({self.menu_item.name} x{self.quantity} = ₱{self.subtotal})"
