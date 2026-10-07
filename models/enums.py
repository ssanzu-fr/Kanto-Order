"""
Enums for order and payment statuses.
"""
from enum import Enum


class OrderStatus(Enum):
    """Order workflow statuses - forward only, no skipping."""
    PENDING_PAYMENT = "Pending Payment"
    CONFIRMED = "Confirmed"
    PREPARING = "Preparing"
    READY = "Ready"
    COMPLETED = "Completed"


class PaymentStatus(Enum):
    """Payment statuses."""
    UNPAID = "Unpaid"
    PAID = "Paid"
