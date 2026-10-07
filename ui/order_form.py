"""
Order form component - customer name, menu, cart, and place order.
"""
import customtkinter as ctk
import os
from typing import Dict, Callable
from PIL import Image
from ui.theme import COLORS, FONT_SIZES, SPACING, SIZES
from ui.fonts import get_font
from data.menu import get_item_by_id, get_menu_by_category
from models.menu_item import MenuItem
from models.order_item import OrderItem


class OrderForm(ctk.CTkFrame):
    """Left panel - create new orders."""

    def __init__(self, parent, on_order_placed: Callable, calculate_total: Callable):
        super().__init__(
            parent,
            fg_color=COLORS["panel"],
            corner_radius=SIZES["corner_radius"]
        )

        self.on_order_placed = on_order_placed
        self.calculate_total = calculate_total
        self.cart: Dict[str, int] = {}  # {menu_item_id: quantity}
        self.menu_by_category = get_menu_by_category()
        self.quantity_labels = {}
        self.active_category = None

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the order form UI."""
        self.main_view = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_view = ctk.CTkFrame(self, fg_color="transparent")

        self._build_main_view()
        self._build_menu_view()
        self._show_main_view()

    def _build_main_view(self) -> None:
        """Build the simple main order screen."""
        self.main_view.grid_columnconfigure(0, weight=1)
        self.main_view.grid_rowconfigure(1, weight=1)

        top_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="ew")

        cart_area = ctk.CTkFrame(self.main_view, fg_color="transparent")
        cart_area.grid(row=1, column=0, sticky="nsew")
        cart_area.grid_columnconfigure(0, weight=1)
        cart_area.grid_rowconfigure(1, weight=1)

        bottom_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        bottom_frame.grid(row=2, column=0, sticky="ew")

        # Header
        header_label = ctk.CTkLabel(
            top_frame,
            text="NEW ORDER",
            font=get_font("heading", FONT_SIZES["heading"], "bold"),
            text_color=COLORS["primary"]
        )
        header_label.pack(pady=(SPACING["lg"], SPACING["md"]), padx=SPACING["lg"], anchor="w")

        # Customer name input
        name_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        name_frame.pack(fill="x", padx=SPACING["lg"], pady=(0, SPACING["md"]))

        ctk.CTkLabel(
            name_frame,
            text="Customer:",
            font=get_font("body", FONT_SIZES["body"]),
            text_color=COLORS["text"]
        ).pack(anchor="w")

        self.customer_name_entry = ctk.CTkEntry(
            name_frame,
            height=SIZES["input_height"],
            font=get_font("body", FONT_SIZES["body"]),
            fg_color=COLORS["input_bg"],
            border_color=COLORS["border"],
            text_color=COLORS["text"]
        )
        self.customer_name_entry.pack(fill="x", pady=(SPACING["xs"], 0))

        # Payment and submit stay near the top so they are always visible.
        payment_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        payment_frame.pack(fill="x", padx=SPACING["lg"], pady=(0, SPACING["md"]))

        ctk.CTkLabel(
            payment_frame,
            text="Payment:",
            font=get_font("body", FONT_SIZES["body"]),
            text_color=COLORS["text"]
        ).pack(side="left")

        self.payment_var = ctk.StringVar(value="now")

        self.pay_now_radio = ctk.CTkRadioButton(
            payment_frame,
            text="Pay now",
            variable=self.payment_var,
            value="now",
            font=get_font("body", FONT_SIZES["body"]),
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color=COLORS["text"]
        )
        self.pay_now_radio.pack(side="left", padx=(SPACING["md"], 0))

        self.pay_later_radio = ctk.CTkRadioButton(
            payment_frame,
            text="Pay later",
            variable=self.payment_var,
            value="later",
            font=get_font("body", FONT_SIZES["body"]),
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color=COLORS["text"]
        )
        self.pay_later_radio.pack(side="left", padx=(SPACING["md"], 0))

        self.choose_food_btn = ctk.CTkButton(
            top_frame,
            text="CHOOSE FOOD",
            height=SIZES["button_height"],
            font=get_font("body", FONT_SIZES["body"], "bold"),
            fg_color=COLORS["secondary"],
            hover_color=COLORS["secondary_hover"],
            text_color=COLORS["text"],
            command=self._show_menu_view
        )
        self.choose_food_btn.pack(fill="x", padx=SPACING["lg"], pady=(0, SPACING["md"]))

        cart_header = ctk.CTkLabel(
            cart_area,
            text="Cart",
            font=get_font("body", FONT_SIZES["subheading"], "bold"),
            text_color=COLORS["text"]
        )
        cart_header.grid(row=0, column=0, sticky="w", padx=SPACING["lg"], pady=(SPACING["sm"], SPACING["sm"]))

        self.cart_frame = ctk.CTkFrame(
            cart_area,
            fg_color=COLORS["input_bg"]
        )
        self.cart_frame.grid(row=1, column=0, sticky="nsew", padx=SPACING["lg"], pady=(0, SPACING["md"]))

        self.cart_scroll = ctk.CTkScrollableFrame(
            self.cart_frame,
            fg_color="transparent"
        )
        self.cart_scroll.pack(fill="both", expand=True, padx=SPACING["sm"], pady=SPACING["sm"])

        self.total_label = ctk.CTkLabel(
            bottom_frame,
            text="Total: ₱0",
            font=get_font("body", FONT_SIZES["subheading"], "bold"),
            text_color=COLORS["primary"]
        )
        self.total_label.pack(pady=(0, SPACING["md"]), padx=SPACING["lg"], anchor="w")

        self.place_order_btn = ctk.CTkButton(
            bottom_frame,
            text="PLACE ORDER",
            height=SIZES["button_height"],
            font=get_font("body", FONT_SIZES["body"], "bold"),
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color=COLORS["background"],
            command=self._place_order
        )
        self.place_order_btn.pack(fill="x", padx=SPACING["lg"], pady=(0, SPACING["lg"]))

        self._update_cart_display()

    def _build_menu_view(self) -> None:
        """Build the food picker screen."""
        self.menu_view.grid_columnconfigure(0, weight=1)
        self.menu_view.grid_rowconfigure(2, weight=1)

        menu_header = ctk.CTkFrame(self.menu_view, fg_color="transparent")
        menu_header.grid(row=0, column=0, sticky="ew", padx=SPACING["lg"], pady=(SPACING["lg"], SPACING["md"]))

        ctk.CTkLabel(
            menu_header,
            text="CHOOSE FOOD",
            font=get_font("heading", FONT_SIZES["heading"], "bold"),
            text_color=COLORS["primary"]
        ).pack(side="left")

        # Category tabs
        self.category_frame = ctk.CTkFrame(self.menu_view, fg_color="transparent")
        self.category_frame.grid(row=1, column=0, sticky="ew", padx=SPACING["lg"], pady=(0, SPACING["sm"]))

        self.category_buttons = {}

        for idx, category in enumerate(self.menu_by_category.keys()):
            btn = ctk.CTkButton(
                self.category_frame,
                text=category.split()[0] if len(category.split()) > 1 else category,
                height=32,
                font=get_font("body", FONT_SIZES["small"]),
                fg_color=COLORS["button_bg"],
                hover_color=COLORS["panel_hover"],
                text_color=COLORS["text"],
                command=lambda c=category: self._switch_category(c)
            )
            btn.pack(side="left", padx=(0, SPACING["xs"]))
            self.category_buttons[category] = btn

        # Menu items scrollable area
        self.menu_scroll = ctk.CTkScrollableFrame(
            self.menu_view,
            fg_color="transparent"
        )
        self.menu_scroll.grid(row=2, column=0, sticky="nsew", padx=SPACING["lg"], pady=(0, SPACING["md"]))

        menu_footer = ctk.CTkFrame(
            self.menu_view,
            fg_color=COLORS["input_bg"],
            corner_radius=SIZES["corner_radius"]
        )
        menu_footer.grid(row=3, column=0, sticky="ew", padx=SPACING["lg"], pady=(0, SPACING["lg"]))
        menu_footer.grid_columnconfigure(0, weight=1)

        self.menu_total_label = ctk.CTkLabel(
            menu_footer,
            text="Cart: 0 items | Total: ₱0",
            font=get_font("body", FONT_SIZES["body"], "bold"),
            text_color=COLORS["primary"]
        )
        self.menu_total_label.grid(row=0, column=0, sticky="w", padx=SPACING["md"], pady=SPACING["md"])

        self.menu_back_order_btn = ctk.CTkButton(
            menu_footer,
            text="Back to Order",
            width=120,
            height=34,
            font=get_font("body", FONT_SIZES["small"], "bold"),
            fg_color=COLORS["button_bg"],
            hover_color=COLORS["panel_hover"],
            text_color=COLORS["text"],
            command=self._show_main_view
        )
        self.menu_back_order_btn.grid(row=0, column=1, sticky="e", padx=SPACING["md"], pady=SPACING["md"])

        # Show first category by default
        first_category = list(self.menu_by_category.keys())[0]
        self._switch_category(first_category)

    def _show_main_view(self) -> None:
        """Show order details and cart."""
        self.menu_view.pack_forget()
        self.main_view.pack(fill="both", expand=True)

    def _show_menu_view(self) -> None:
        """Show food picker."""
        self.main_view.pack_forget()
        self.menu_view.pack(fill="both", expand=True)

    def _switch_category(self, category: str) -> None:
        """Switch to a different menu category."""
        self.active_category = category

        # Update button colors
        for cat, btn in self.category_buttons.items():
            if cat == category:
                btn.configure(fg_color=COLORS["primary"], text_color=COLORS["background"])
            else:
                btn.configure(fg_color=COLORS["button_bg"], text_color=COLORS["text"])

        # Clear and rebuild menu items
        for widget in self.menu_scroll.winfo_children():
            widget.destroy()
        self.quantity_labels = {}

        items = self.menu_by_category[category]
        for item in items:
            self._create_menu_item_row(item)

    def _create_menu_item_row(self, item: MenuItem) -> None:
        """Create a row for a menu item with quantity controls."""
        row = ctk.CTkFrame(
            self.menu_scroll,
            fg_color=COLORS["input_bg"],
            corner_radius=SIZES["corner_radius"]
        )
        row.pack(fill="x", pady=SPACING["sm"])

        image_frame = ctk.CTkFrame(
            row,
            fg_color=COLORS["panel_hover"],
            width=78,
            height=64,
            corner_radius=SIZES["corner_radius"]
        )
        image_frame.pack(side="left", padx=SPACING["md"], pady=SPACING["md"])
        image_frame.pack_propagate(False)

        image_path = self._get_menu_image_path(item.id)
        if image_path:
            menu_image = Image.open(image_path)
            menu_photo = ctk.CTkImage(
                light_image=menu_image,
                dark_image=menu_image,
                size=(78, 64)
            )
            ctk.CTkLabel(image_frame, image=menu_photo, text="").pack(expand=True)
        else:
            ctk.CTkLabel(
                image_frame,
                text="IMG",
                font=get_font("body", FONT_SIZES["small"], "bold"),
                text_color=COLORS["text_dim"]
            ).pack(expand=True)

        # Item name and price
        info_frame = ctk.CTkFrame(row, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            info_frame,
            text=item.name,
            font=get_font("body", FONT_SIZES["body"]),
            text_color=COLORS["text"],
            anchor="w"
        ).pack(side="left")

        ctk.CTkLabel(
            info_frame,
            text=f"₱{item.price}",
            font=get_font("body", FONT_SIZES["body"]),
            text_color=COLORS["text_dim"],
            anchor="w"
        ).pack(side="left", padx=(SPACING["sm"], 0))

        # Quantity controls
        controls_frame = ctk.CTkFrame(row, fg_color="transparent")
        controls_frame.pack(side="right")

        # Minus button
        minus_btn = ctk.CTkButton(
            controls_frame,
            text="-",
            width=30,
            height=30,
            font=get_font("body", FONT_SIZES["body"], "bold"),
            fg_color=COLORS["button_bg"],
            hover_color=COLORS["panel_hover"],
            text_color=COLORS["text"],
            command=lambda: self._decrease_quantity(item)
        )
        minus_btn.pack(side="left", padx=(0, SPACING["xs"]))

        # Quantity label
        qty = self.cart.get(item.id, 0)
        qty_label = ctk.CTkLabel(
            controls_frame,
            text=str(qty),
            width=30,
            font=get_font("body", FONT_SIZES["body"]),
            text_color=COLORS["text"]
        )
        qty_label.pack(side="left")

        # Store reference for updates
        if not hasattr(self, 'quantity_labels'):
            self.quantity_labels = {}
        self.quantity_labels[item.id] = qty_label

        # Plus button
        plus_btn = ctk.CTkButton(
            controls_frame,
            text="+",
            width=30,
            height=30,
            font=get_font("body", FONT_SIZES["body"], "bold"),
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color=COLORS["background"],
            command=lambda: self._increase_quantity(item)
        )
        plus_btn.pack(side="left", padx=(SPACING["xs"], 0))

    def _get_menu_image_path(self, item_id: str) -> str | None:
        """Return a local menu image path if one exists."""
        image_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets",
            "images",
            "menu"
        )

        for extension in ("png", "jpg", "jpeg"):
            path = os.path.join(image_dir, f"{item_id}.{extension}")
            if os.path.exists(path):
                return path
        return None

    def _increase_quantity(self, item: MenuItem) -> None:
        """Increase quantity of an item in the cart."""
        current = self.cart.get(item.id, 0)
        self.cart[item.id] = current + 1
        self._update_quantity_display(item.id)
        self._update_cart_display()

    def _decrease_quantity(self, item: MenuItem) -> None:
        """Decrease quantity of an item in the cart."""
        current = self.cart.get(item.id, 0)
        if current > 0:
            self.cart[item.id] = current - 1
            if self.cart[item.id] == 0:
                del self.cart[item.id]
            self._update_quantity_display(item.id)
            self._update_cart_display()

    def _update_quantity_display(self, item_id: str) -> None:
        """Update the quantity label for an item."""
        if hasattr(self, 'quantity_labels') and item_id in self.quantity_labels:
            qty = self.cart.get(item_id, 0)
            self.quantity_labels[item_id].configure(text=str(qty))

    def _update_cart_display(self) -> None:
        """Update the cart display and total."""
        # Clear cart display
        for widget in self.cart_scroll.winfo_children():
            widget.destroy()

        if not self.cart:
            ctk.CTkLabel(
                self.cart_scroll,
                text="Cart is empty",
                font=get_font("body", FONT_SIZES["small"]),
                text_color=COLORS["text_dim"]
            ).pack(pady=SPACING["md"])
            self.total_label.configure(text="Total: ₱0")
            self.choose_food_btn.configure(text="CHOOSE FOOD (0 items)")
            if hasattr(self, "menu_total_label"):
                self.menu_total_label.configure(text="Cart: 0 items | Total: ₱0")
            return

        # Show cart items
        order_items = []
        for item_id, qty in self.cart.items():
            item = get_item_by_id(item_id)
            if item:
                order_item = OrderItem(menu_item=item, quantity=qty)
                order_items.append(order_item)

                row = ctk.CTkFrame(self.cart_scroll, fg_color="transparent")
                row.pack(fill="x", pady=SPACING["xs"])

                ctk.CTkLabel(
                    row,
                    text=f"{item.name} x{qty}",
                    font=get_font("body", FONT_SIZES["small"]),
                    text_color=COLORS["text"],
                    anchor="w"
                ).pack(side="left")

                ctk.CTkLabel(
                    row,
                    text=f"₱{order_item.subtotal}",
                    font=get_font("body", FONT_SIZES["small"]),
                    text_color=COLORS["text"],
                    anchor="e"
                ).pack(side="right")

        total = self.calculate_total(order_items)
        self.total_label.configure(text=f"Total: ₱{total}")
        total_items = sum(self.cart.values())
        self.choose_food_btn.configure(text=f"CHOOSE FOOD ({total_items} items)")
        if hasattr(self, "menu_total_label"):
            self.menu_total_label.configure(text=f"Cart: {total_items} items | Total: ₱{total}")

    def _place_order(self) -> None:
        """Validate and place the order."""
        # Validate customer name
        customer_name = self.customer_name_entry.get().strip()
        if not customer_name:
            self._show_error("Please enter customer name")
            return

        # Validate cart
        if not self.cart:
            self._show_error("Please add items to cart")
            return

        # Get payment option
        pay_now = self.payment_var.get() == "now"

        # Call the callback
        self.on_order_placed(customer_name, self.cart, pay_now)

        # Clear the form
        self._clear_form()

    def _clear_form(self) -> None:
        """Clear the form after placing an order."""
        self.customer_name_entry.delete(0, 'end')
        self.cart.clear()
        self.payment_var.set("now")

        # Reset quantity displays
        if hasattr(self, 'quantity_labels'):
            for label in self.quantity_labels.values():
                if label.winfo_exists():
                    label.configure(text="0")

        self._update_cart_display()
        if self.active_category:
            self._switch_category(self.active_category)
        self._show_main_view()

    def _show_error(self, message: str) -> None:
        """Show an error message."""
        # Create a simple popup
        popup = ctk.CTkToplevel(self)
        popup.title("Error")
        popup.geometry("300x150")
        popup.configure(fg_color=COLORS["panel"])

        ctk.CTkLabel(
            popup,
            text=message,
            font=get_font("body", FONT_SIZES["body"]),
            text_color=COLORS["error"]
        ).pack(pady=SPACING["lg"])

        ctk.CTkButton(
            popup,
            text="OK",
            command=popup.destroy,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color=COLORS["background"]
        ).pack(pady=SPACING["md"])

        # Center the popup
        popup.transient(self)
        popup.grab_set()
