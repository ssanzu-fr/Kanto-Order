"""
Order list component - displays all orders with status and actions.
"""
import customtkinter as ctk
from typing import List, Callable, Optional
from PIL import Image
import os
from ui.theme import COLORS, FONT_SIZES, SPACING, SIZES
from ui.fonts import get_font
from models.order import Order
from models.enums import OrderStatus, PaymentStatus


class OrderList(ctk.CTkFrame):
    """Right panel - list of orders with filters and actions."""

    def __init__(self, parent, orders: List[Order], on_order_selected: Callable,
                 on_order_updated: Callable):
        super().__init__(
            parent,
            fg_color=COLORS["panel"],
            corner_radius=SIZES["corner_radius"]
        )

        self.orders = orders
        self.on_order_selected = on_order_selected
        self.on_order_updated = on_order_updated
        self.selected_order: Optional[Order] = None

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the order list UI."""

        # Header with filter
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=SPACING["lg"], pady=(SPACING["lg"], SPACING["sm"]))

        ctk.CTkLabel(
            header_frame,
            text="ORDERS",
            font=get_font("heading", FONT_SIZES["heading"], "bold"),
            text_color=COLORS["primary"]
        ).pack(side="left")

        # Status filter
        self.filter_var = ctk.StringVar(value="All")
        filter_options = ["All", "Pending Payment", "Confirmed", "Preparing", "Ready", "Completed"]

        self.filter_menu = ctk.CTkOptionMenu(
            header_frame,
            values=filter_options,
            variable=self.filter_var,
            font=get_font("body", FONT_SIZES["small"]),
            fg_color=COLORS["button_bg"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_hover"],
            dropdown_fg_color=COLORS["panel"],
            text_color=COLORS["text"],
            command=self._on_filter_changed
        )
        self.filter_menu.pack(side="right")

        # Scrollable order list
        self.order_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.order_scroll.pack(fill="both", expand=True, padx=SPACING["lg"], pady=(0, SPACING["lg"]))

        # Initial render
        self.refresh()

    def _on_filter_changed(self, value: str) -> None:
        """Handle filter change."""
        self.refresh()

    def refresh(self) -> None:
        """Refresh the order list display."""
        # Clear current list
        for widget in self.order_scroll.winfo_children():
            widget.destroy()

        # Filter orders
        filter_value = self.filter_var.get()
        filtered_orders = self.orders if filter_value == "All" else [
            o for o in self.orders if o.status.value == filter_value
        ]

        # Show orders
        if not filtered_orders:
            empty_frame = ctk.CTkFrame(self.order_scroll, fg_color="transparent")
            empty_frame.pack(pady=SPACING["xl"])

            # Small bat icon
            bat_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "assets", "images", "bat_small.png"
            )
            if os.path.exists(bat_path):
                bat_image = Image.open(bat_path)
                bat_photo = ctk.CTkImage(
                    light_image=bat_image,
                    dark_image=bat_image,
                    size=(32, 32)
                )
                ctk.CTkLabel(
                    empty_frame,
                    image=bat_photo,
                    text=""
                ).pack(pady=(0, SPACING["sm"]))

            ctk.CTkLabel(
                empty_frame,
                text="No orders yet",
                font=get_font("body", FONT_SIZES["body"]),
                text_color=COLORS["text_dim"]
            ).pack()
        else:
            for order in reversed(filtered_orders):  # Most recent first
                self._create_order_card(order)

    def _create_order_card(self, order: Order) -> None:
        """Create a card for an order."""
        # Determine if this order is selected
        is_selected = self.selected_order == order

        # Card frame with hover effect
        card = ctk.CTkFrame(
            self.order_scroll,
            fg_color=COLORS["card_selected"] if is_selected else COLORS["input_bg"],
            corner_radius=SIZES["corner_radius"]
        )
        card.pack(fill="x", pady=SPACING["sm"])

        # Store reference for hover effects
        card._original_color = COLORS["card_selected"] if is_selected else COLORS["input_bg"]
        card._hover_color = COLORS["panel_hover"]

        # Hover events
        def on_enter(e):
            if not is_selected:
                card.configure(fg_color=COLORS["panel_hover"])

        def on_leave(e):
            card.configure(fg_color=card._original_color)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        # Make card clickable
        card.bind("<Button-1>", lambda e: self._select_order(order))

        # Order header
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=SPACING["md"], pady=(SPACING["md"], SPACING["xs"]))

        # Order number and customer
        info_frame = ctk.CTkFrame(header, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)

        order_label = ctk.CTkLabel(
            info_frame,
            text=f"#{order.order_number} {order.customer_name}",
            font=get_font("body", FONT_SIZES["body"], "bold"),
            text_color=COLORS["text"],
            anchor="w"
        )
        order_label.pack(anchor="w")
        order_label.bind("<Button-1>", lambda e: self._select_order(order))

        # Payment badge
        payment_color = COLORS["success"] if order.payment.status == PaymentStatus.PAID else COLORS["warning"]
        payment_text = "PAID" if order.payment.status == PaymentStatus.PAID else "UNPAID"

        payment_badge = ctk.CTkLabel(
            header,
            text=payment_text,
            font=get_font("body", FONT_SIZES["small"], "bold"),
            text_color=payment_color,
            width=60
        )
        payment_badge.pack(side="right")

        # Order items
        items_text = ", ".join([f"{item.menu_item.name} x{item.quantity}" for item in order.items])
        items_label = ctk.CTkLabel(
            card,
            text=items_text,
            font=get_font("body", FONT_SIZES["small"]),
            text_color=COLORS["text_dim"],
            anchor="w"
        )
        items_label.pack(fill="x", padx=SPACING["md"], pady=(0, SPACING["xs"]))
        items_label.bind("<Button-1>", lambda e: self._select_order(order))

        # Total
        total_label = ctk.CTkLabel(
            card,
            text=f"₱{order.total}",
            font=get_font("body", FONT_SIZES["body"], "bold"),
            text_color=COLORS["text"],
            anchor="w"
        )
        total_label.pack(fill="x", padx=SPACING["md"], pady=(0, SPACING["xs"]))
        total_label.bind("<Button-1>", lambda e: self._select_order(order))

        # Status and action
        footer = ctk.CTkFrame(card, fg_color="transparent")
        footer.pack(fill="x", padx=SPACING["md"], pady=(SPACING["xs"], SPACING["md"]))

        # Status badge
        status_color = self._get_status_color(order.status)
        status_badge = ctk.CTkLabel(
            footer,
            text=order.status.value.upper(),
            font=get_font("body", FONT_SIZES["small"], "bold"),
            text_color=status_color
        )
        status_badge.pack(side="left")

        # Action button
        action_btn = self._get_action_button(footer, order)
        if action_btn:
            action_btn.pack(side="right")

    def _get_status_color(self, status: OrderStatus) -> str:
        """Get color for status badge."""
        color_map = {
            OrderStatus.PENDING_PAYMENT: COLORS["status_pending"],
            OrderStatus.CONFIRMED: COLORS["status_confirmed"],
            OrderStatus.PREPARING: COLORS["status_preparing"],
            OrderStatus.READY: COLORS["status_ready"],
            OrderStatus.COMPLETED: COLORS["status_completed"]
        }
        return color_map.get(status, COLORS["text"])

    def _get_action_button(self, parent, order: Order) -> Optional[ctk.CTkButton]:
        """Get the appropriate action button for an order."""
        if order.status == OrderStatus.PENDING_PAYMENT:
            return ctk.CTkButton(
                parent,
                text="Mark as Paid",
                height=28,
                font=get_font("body", FONT_SIZES["small"]),
                fg_color=COLORS["success"],
                hover_color=COLORS["success"],
                text_color=COLORS["text"],
                command=lambda: self._mark_as_paid(order)
            )
        elif order.status == OrderStatus.CONFIRMED:
            return ctk.CTkButton(
                parent,
                text="Start Preparing",
                height=28,
                font=get_font("body", FONT_SIZES["small"]),
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_hover"],
                text_color=COLORS["background"],
                command=lambda: self._start_preparing(order)
            )
        elif order.status == OrderStatus.PREPARING:
            return ctk.CTkButton(
                parent,
                text="Mark Ready",
                height=28,
                font=get_font("body", FONT_SIZES["small"]),
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_hover"],
                text_color=COLORS["background"],
                command=lambda: self._mark_ready(order)
            )
        elif order.status == OrderStatus.READY:
            return ctk.CTkButton(
                parent,
                text="Complete Order",
                height=28,
                font=get_font("body", FONT_SIZES["small"]),
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_hover"],
                text_color=COLORS["background"],
                command=lambda: self._complete_order(order)
            )
        return None

    def _select_order(self, order: Order) -> None:
        """Select an order and show its receipt."""
        self.selected_order = order
        self.on_order_selected(order)
        # Refresh to update selected state
        self.refresh()

    def _mark_as_paid(self, order: Order) -> None:
        """Mark order as paid."""
        self.on_order_updated(order, "mark_paid")

    def _start_preparing(self, order: Order) -> None:
        """Start preparing order."""
        self.on_order_updated(order, "start_preparing")

    def _mark_ready(self, order: Order) -> None:
        """Mark order as ready."""
        self.on_order_updated(order, "mark_ready")

    def _complete_order(self, order: Order) -> None:
        """Complete order."""
        self.on_order_updated(order, "complete")
