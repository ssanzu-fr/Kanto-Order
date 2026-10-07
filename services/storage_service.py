"""
StorageService - handles saving and loading orders to/from JSON.
"""
import json
import os
from typing import List
from models.order import Order
from models.order_item import OrderItem
from models.payment import Payment
from models.menu_item import MenuItem
from models.enums import OrderStatus, PaymentStatus
from data.menu import get_item_by_id


class StorageService:
    """Service for persisting orders to JSON file."""

    def __init__(self, data_dir: str | None = None):
        if data_dir is None:
            app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(app_root, "data")

        self.data_dir = data_dir
        self.orders_file = os.path.join(data_dir, "orders.json")
        self._ensure_data_dir()

    def _ensure_data_dir(self) -> None:
        """Create data directory if it doesn't exist."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def save_orders(self, orders: List[Order]) -> None:
        """Save all orders to JSON file."""
        try:
            orders_data = [self._order_to_dict(order) for order in orders]

            with open(self.orders_file, 'w', encoding='utf-8') as f:
                json.dump(orders_data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            raise IOError(f"Failed to save orders: {str(e)}")

    def load_orders(self) -> List[Order]:
        """
        Load all orders from JSON file.
        Returns empty list if file doesn't exist.
        Handles corrupted JSON gracefully.
        """
        if not os.path.exists(self.orders_file):
            return []

        try:
            with open(self.orders_file, 'r', encoding='utf-8') as f:
                orders_data = json.load(f)

            orders = [self._dict_to_order(order_dict) for order_dict in orders_data]
            return orders

        except json.JSONDecodeError:
            print(f"Warning: {self.orders_file} is corrupted. Starting with empty order list.")
            return []

        except Exception as e:
            print(f"Warning: Failed to load orders: {str(e)}. Starting with empty order list.")
            return []

    def get_highest_order_number(self, orders: List[Order]) -> int:
        """Get the highest order number from a list of orders."""
        if not orders:
            return 0

        # Extract numeric part from order numbers
        numbers = []
        for order in orders:
            try:
                numbers.append(int(order.order_number))
            except ValueError:
                continue

        return max(numbers) if numbers else 0

    def _order_to_dict(self, order: Order) -> dict:
        """Convert Order object to dictionary for JSON serialization."""
        return {
            "order_number": order.order_number,
            "customer_name": order.customer_name,
            "items": [
                {
                    "menu_item_id": item.menu_item.id,
                    "quantity": item.quantity
                }
                for item in order.items
            ],
            "payment": {
                "amount": order.payment.amount,
                "status": order.payment.status.value
            },
            "status": order.status.value
        }

    def _dict_to_order(self, data: dict) -> Order:
        """Convert dictionary to Order object."""
        # Reconstruct order items
        items = []
        for item_data in data["items"]:
            menu_item = get_item_by_id(item_data["menu_item_id"])
            if menu_item:
                items.append(OrderItem(
                    menu_item=menu_item,
                    quantity=item_data["quantity"]
                ))

        # Reconstruct payment
        payment = Payment(
            amount=data["payment"]["amount"],
            status=PaymentStatus(data["payment"]["status"])
        )

        # Reconstruct order
        order = Order(
            order_number=data["order_number"],
            customer_name=data["customer_name"],
            items=items,
            payment=payment,
            status=OrderStatus(data["status"])
        )

        return order
