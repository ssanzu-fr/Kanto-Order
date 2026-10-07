"""
Receipt view component - displays order details in the required format.
"""
import customtkinter as ctk
from typing import Optional
from ui.theme import COLORS, FONT_SIZES, SPACING
from ui.fonts import get_font
from ui.receipt_formatter import format_receipt
from models.order import Order


class ReceiptView(ctk.CTkFrame):
    """Bottom panel - shows receipt for selected order."""

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color=COLORS["panel"],
            corner_radius=SPACING["sm"],
            height=150
        )
        self.pack_propagate(False)

        self.current_order: Optional[Order] = None
        self._build_ui()

    def _build_ui(self) -> None:
        """Build the receipt UI."""
        # Header
        header_label = ctk.CTkLabel(
            self,
            text="RECEIPT",
            font=get_font("heading", FONT_SIZES["subheading"], "bold"),
            text_color=COLORS["primary"]
        )
        header_label.pack(pady=(SPACING["md"], SPACING["sm"]), padx=SPACING["lg"], anchor="w")

        # Receipt content frame
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=SPACING["lg"], pady=(0, SPACING["md"]))

        # Show empty message initially
        self._show_empty()

    def _show_empty(self) -> None:
        """Show empty state."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.content_frame,
            text="Select an order to view receipt",
            font=get_font("body", FONT_SIZES["body"]),
            text_color=COLORS["text_dim"]
        ).pack(pady=SPACING["md"])

    def show_order(self, order: Order) -> None:
        """
        Display order receipt in the required format:

        Customer: Maria Santos
        Order No.: 001
        Food: Chicken Meal
        Price: ₱120
        Payment: PAID
        Order Status: COMPLETED
        """
        self.current_order = order

        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        receipt_text = format_receipt(order)

        # Display receipt
        receipt_label = ctk.CTkLabel(
            self.content_frame,
            text=receipt_text,
            font=get_font("body", FONT_SIZES["body"]),
            text_color=COLORS["text"],
            justify="left",
            anchor="w"
        )
        receipt_label.pack(anchor="w", pady=SPACING["sm"])

    def clear(self) -> None:
        """Clear the receipt view."""
        self.current_order = None
        self._show_empty()
