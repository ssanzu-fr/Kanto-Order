"""
WorkflowService - enforces the business process rules.
Forward-only status transitions, unpaid orders cannot be prepared.
"""
from models.order import Order
from models.enums import OrderStatus, PaymentStatus


class WorkflowService:
    """Service for managing order workflow and status transitions."""

    # Define allowed transitions
    _ALLOWED_TRANSITIONS = {
        OrderStatus.PENDING_PAYMENT: [OrderStatus.CONFIRMED],
        OrderStatus.CONFIRMED: [OrderStatus.PREPARING],
        OrderStatus.PREPARING: [OrderStatus.READY],
        OrderStatus.READY: [OrderStatus.COMPLETED],
        OrderStatus.COMPLETED: []  # No transitions from completed
    }

    def can_transition(self, order: Order, new_status: OrderStatus) -> tuple[bool, str]:
        """
        Check if an order can transition to a new status.

        Returns:
            Tuple of (can_transition: bool, reason: str)
        """
        current_status = order.status

        # Cannot transition from completed
        if current_status == OrderStatus.COMPLETED:
            return False, "Order is already completed"

        # Check if transition is allowed
        if new_status not in self._ALLOWED_TRANSITIONS[current_status]:
            return False, f"Cannot go from {current_status.value} to {new_status.value}"

        # Special rule: unpaid orders cannot be prepared
        if new_status in [OrderStatus.PREPARING, OrderStatus.READY, OrderStatus.COMPLETED]:
            if order.payment.status == PaymentStatus.UNPAID:
                return False, "Unpaid orders cannot be prepared"

        return True, ""

    def transition_to(self, order: Order, new_status: OrderStatus) -> None:
        """
        Transition an order to a new status.
        Raises ValueError if transition is not allowed.
        """
        can_transition, reason = self.can_transition(order, new_status)

        if not can_transition:
            raise ValueError(reason)

        order.status = new_status

    def start_preparing(self, order: Order) -> None:
        """Move order from CONFIRMED to PREPARING."""
        self.transition_to(order, OrderStatus.PREPARING)

    def mark_ready(self, order: Order) -> None:
        """Move order from PREPARING to READY."""
        self.transition_to(order, OrderStatus.READY)

    def complete_order(self, order: Order) -> None:
        """Move order from READY to COMPLETED."""
        self.transition_to(order, OrderStatus.COMPLETED)

    def get_next_status(self, order: Order) -> OrderStatus:
        """Get the next allowed status for an order."""
        allowed = self._ALLOWED_TRANSITIONS[order.status]
        if allowed:
            return allowed[0]
        return None
