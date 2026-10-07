"""
Main application window and layout.
"""
import customtkinter as ctk
from ui.theme import COLORS, SPACING
from ui.header import Header
from ui.order_form import OrderForm
from ui.order_list import OrderList
from ui.receipt_view import ReceiptView
from services.order_service import OrderService
from services.payment_service import PaymentService
from services.workflow_service import WorkflowService
from services.storage_service import StorageService
from models.order_item import OrderItem
from models.order import Order
from data.menu import get_item_by_id


class App(ctk.CTk):
    """Main application window."""

    WINDOW_WIDTH = 1120
    WINDOW_HEIGHT = 720

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Kanto Orders")
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.minsize(980, 640)

        # Set color theme
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=COLORS["background"])

        # Initialize services
        self.order_service = OrderService()
        self.payment_service = PaymentService()
        self.workflow_service = WorkflowService()
        self.storage_service = StorageService()

        # Load existing orders
        self.orders = self.storage_service.load_orders()
        highest_num = self.storage_service.get_highest_order_number(self.orders)
        self.order_service.set_next_order_number(highest_num + 1)

        # Build layout
        self._build_layout()

        # Update header with order count
        self.header.update_order_count(len(self.orders))
        self.after(0, self._center_window)

    def _center_window(self) -> None:
        """Center the app on the current screen."""
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = max((screen_width - self.WINDOW_WIDTH) // 2, 0)
        y = max((screen_height - self.WINDOW_HEIGHT) // 2, 0)
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x}+{y}")

    def _handle_order_selected(self, order: Order) -> None:
        """Handle an order being selected from the list."""
        self.receipt_view.show_order(order)

    def _handle_order_updated(self, order: Order, action: str) -> None:
        """Handle order status update actions."""
        try:
            if action == "mark_paid":
                self.payment_service.mark_as_paid(order)
            elif action == "start_preparing":
                self.workflow_service.start_preparing(order)
            elif action == "mark_ready":
                self.workflow_service.mark_ready(order)
            elif action == "complete":
                self.workflow_service.complete_order(order)

            # Save updated orders
            self.storage_service.save_orders(self.orders)

            # Refresh order list and receipt
            self.order_list.refresh()
            if self.order_list.selected_order == order:
                self.receipt_view.show_order(order)

        except ValueError as e:
            self._show_error(str(e))

    def _build_layout(self) -> None:
        """Build the main layout structure."""

        # Header at the top
        self.header = Header(self)
        self.header.pack(fill="x", padx=0, pady=0)

        # Main content area
        self.content_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS["background"]
        )
        self.content_frame.pack(fill="both", expand=True, padx=SPACING["lg"], pady=SPACING["lg"])
        self.content_frame.grid_columnconfigure(0, weight=1, uniform="main")
        self.content_frame.grid_columnconfigure(1, weight=1, uniform="main")
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Left panel: Order form
        self.order_form = OrderForm(
            self.content_frame,
            on_order_placed=self._handle_order_placed,
            calculate_total=self.order_service.calculate_total
        )
        self.order_form.grid(row=0, column=0, sticky="nsew", padx=(0, SPACING["md"]))

        # Right panel: Order list
        self.order_list = OrderList(
            self.content_frame,
            orders=self.orders,
            on_order_selected=self._handle_order_selected,
            on_order_updated=self._handle_order_updated
        )
        self.order_list.grid(row=0, column=1, sticky="nsew")

        # Bottom panel: Receipt
        self.receipt_view = ReceiptView(self)
        self.receipt_view.pack(fill="x", padx=SPACING["lg"], pady=(0, SPACING["lg"]))

    def _center_popup(self, popup: ctk.CTkToplevel, width: int, height: int) -> None:
        """Center a popup over the app window."""
        self.update_idletasks()
        x = self.winfo_x() + max((self.winfo_width() - width) // 2, 0)
        y = self.winfo_y() + max((self.winfo_height() - height) // 2, 0)
        popup.geometry(f"{width}x{height}+{x}+{y}")

    def _handle_order_placed(self, customer_name: str, cart: dict, pay_now: bool) -> None:
        """Handle a new order being placed."""
        # Convert cart to OrderItems
        order_items = []
        for item_id, quantity in cart.items():
            menu_item = get_item_by_id(item_id)
            if menu_item:
                order_items.append(OrderItem(menu_item=menu_item, quantity=quantity))

        # Create order
        order = self.order_service.create_order(customer_name, order_items, pay_now)

        # Add to orders list
        self.orders.append(order)

        # Save to storage
        self.storage_service.save_orders(self.orders)

        # Update header count
        self.header.update_order_count(len(self.orders))

        # Refresh order list
        self.order_list.refresh()

        # Show success message
        self._show_success(f"Order #{order.order_number} placed for {customer_name}!")

    def _show_success(self, message: str) -> None:
        """Show a success message."""
        popup = ctk.CTkToplevel(self)
        popup.title("Success")
        self._center_popup(popup, 350, 150)
        popup.configure(fg_color=COLORS["panel"])

        ctk.CTkLabel(
            popup,
            text=message,
            font=("Arial", 14),
            text_color=COLORS["success"]
        ).pack(pady=SPACING["lg"])

        ctk.CTkButton(
            popup,
            text="OK",
            command=popup.destroy,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color=COLORS["background"]
        ).pack(pady=SPACING["md"])

        popup.transient(self)
        popup.grab_set()

    def _show_error(self, message: str) -> None:
        """Show an error message."""
        popup = ctk.CTkToplevel(self)
        popup.title("Error")
        self._center_popup(popup, 350, 150)
        popup.configure(fg_color=COLORS["panel"])

        ctk.CTkLabel(
            popup,
            text=message,
            font=("Arial", 14),
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

        popup.transient(self)
        popup.grab_set()
