"""
Receipt text formatting for the required school display.
"""
from models.enums import PaymentStatus
from models.order import Order


def format_receipt(order: Order) -> str:
    """Return receipt text with the six required labels in order."""
    lines = [
        f"Customer: {order.customer_name}",
        f"Order No.: {order.order_number}",
    ]

    if len(order.items) == 1:
        item = order.items[0]
        if item.quantity == 1:
            lines.append(f"Food: {item.menu_item.name}")
            lines.append(f"Price: ₱{item.menu_item.price}")
        else:
            lines.append(f"Food: {item.menu_item.name} x{item.quantity}")
            lines.append(f"Price: ₱{item.subtotal}")
    else:
        lines.append("Food:")
        lines.extend(
            f"  {item.menu_item.name} x{item.quantity} - ₱{item.subtotal}"
            for item in order.items
        )
        lines.append(f"Price: ₱{order.total}")

    payment_status = "PAID" if order.payment.status == PaymentStatus.PAID else "UNPAID"
    lines.append(f"Payment: {payment_status}")
    lines.append(f"Order Status: {order.status.value.upper()}")

    return "\n".join(lines)
