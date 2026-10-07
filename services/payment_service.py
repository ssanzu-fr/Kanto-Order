"""
PaymentService - handles payment status checking and updates.
"""
from models.order import Order
from models.enums import PaymentStatus, OrderStatus


class PaymentService:
    """Service for managing payments."""

    def is_paid(self, order: Order) -> bool:
        """Check if an order is paid."""
        return order.payment.status == PaymentStatus.PAID

    def mark_as_paid(self, order: Order) -> None:
        """
        Mark an order as paid.
        Also updates order status from PENDING_PAYMENT to CONFIRMED.
        """
        if self.is_paid(order):
            raise ValueError("Order is already paid")

        order.payment.status = PaymentStatus.PAID

        # If order was pending payment, move it to confirmed
        if order.status == OrderStatus.PENDING_PAYMENT:
            order.status = OrderStatus.CONFIRMED

    def get_payment_status(self, order: Order) -> PaymentStatus:
        """Get the payment status of an order."""
        return order.payment.status
