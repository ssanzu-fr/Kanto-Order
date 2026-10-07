"""
Order model - the main business entity.
"""
from dataclasses import dataclass, field
from typing import List
from models.enums import OrderStatus
from models.order_item import OrderItem
from models.payment import Payment


@dataclass
class Order:
    """A complete customer order."""
    order_number: str
    customer_name: str
    items: List[OrderItem] = field(default_factory=list)
    payment: Payment = None
    status: OrderStatus = OrderStatus.PENDING_PAYMENT

    @property
    def total(self) -> float:
        """Calculate total from all order items."""
        return sum(item.subtotal for item in self.items)

    def __repr__(self) -> str:
        items_str = ", ".join(f"{item.menu_item.name} x{item.quantity}" for item in self.items)
        return (
            f"Order #{self.order_number}: {self.customer_name}\n"
            f"  Items: {items_str}\n"
            f"  Total: ₱{self.total}\n"
            f"  Payment: {self.payment.status.value if self.payment else 'None'}\n"
            f"  Status: {self.status.value}"
        )
