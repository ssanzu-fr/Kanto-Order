"""
OrderService - handles order creation, item management, and total calculation.
"""
from typing import List
from models.order import Order
from models.order_item import OrderItem
from models.payment import Payment
from models.menu_item import MenuItem
from models.enums import OrderStatus, PaymentStatus


class OrderService:
    """Service for managing orders."""

    def __init__(self):
        self._next_order_number = 1

    def set_next_order_number(self, number: int) -> None:
        """Set the next order number (used when loading from storage)."""
        self._next_order_number = number

    def get_next_order_number(self) -> str:
        """Generate the next order number (zero-padded to 3 digits)."""
        order_num = f"{self._next_order_number:03d}"
        self._next_order_number += 1
        return order_num

    def create_order(self, customer_name: str, items: List[OrderItem], pay_now: bool = False) -> Order:
        """
        Create a new order.

        Args:
            customer_name: Customer's name
            items: List of OrderItem objects
            pay_now: If True, order starts as CONFIRMED with PAID status
                    If False, order starts as PENDING_PAYMENT with UNPAID status

        Returns:
            A new Order object
        """
        if not customer_name or not customer_name.strip():
            raise ValueError("Customer name cannot be empty")

        if not items or len(items) == 0:
            raise ValueError("Order must have at least one item")

        # Calculate total
        total = self.calculate_total(items)

        # Create payment
        if pay_now:
            payment = Payment(amount=total, status=PaymentStatus.PAID)
            status = OrderStatus.CONFIRMED
        else:
            payment = Payment(amount=total, status=PaymentStatus.UNPAID)
            status = OrderStatus.PENDING_PAYMENT

        # Generate order number
        order_number = self.get_next_order_number()

        # Create order
        order = Order(
            order_number=order_number,
            customer_name=customer_name.strip(),
            items=items,
            payment=payment,
            status=status
        )

        return order

    def calculate_total(self, items: List[OrderItem]) -> float:
        """Calculate total amount from order items."""
        return sum(item.subtotal for item in items)

    def add_item(self, order: Order, menu_item: MenuItem, quantity: int) -> None:
        """Add an item to an existing order."""
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        # Check if item already exists in order
        for item in order.items:
            if item.menu_item.id == menu_item.id:
                item.quantity += quantity
                return

        # Add new item
        order.items.append(OrderItem(menu_item=menu_item, quantity=quantity))

    def remove_item(self, order: Order, menu_item_id: str) -> None:
        """Remove an item from an order."""
        order.items = [item for item in order.items if item.menu_item.id != menu_item_id]

    def update_item_quantity(self, order: Order, menu_item_id: str, quantity: int) -> None:
        """Update quantity of an item in the order."""
        if quantity <= 0:
            self.remove_item(order, menu_item_id)
            return

        for item in order.items:
            if item.menu_item.id == menu_item_id:
                item.quantity = quantity
                return
