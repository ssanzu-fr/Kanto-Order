"""
Payment model.
"""
from dataclasses import dataclass
from models.enums import PaymentStatus


@dataclass
class Payment:
    """Payment information for an order."""
    amount: float
    status: PaymentStatus

    def __repr__(self) -> str:
        return f"Payment(₱{self.amount}, {self.status.value})"
