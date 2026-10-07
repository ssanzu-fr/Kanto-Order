"""
Header component - app title and order count.
"""
import customtkinter as ctk
from PIL import Image
import os
from ui.theme import COLORS, FONT_SIZES
from ui.fonts import get_font


class Header(ctk.CTkFrame):
    """Top header with app name and order count."""

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color=COLORS["panel"],
            corner_radius=0
        )

        self.order_count = 0

        # Load bat logo
        logo_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets", "images", "bat_logo.png"
        )

        # Left side: logo and title
        left_frame = ctk.CTkFrame(self, fg_color="transparent")
        left_frame.pack(side="left", padx=20, pady=15)

        # Bat logo
        if os.path.exists(logo_path):
            bat_image = Image.open(logo_path)
            bat_photo = ctk.CTkImage(
                light_image=bat_image,
                dark_image=bat_image,
                size=(40, 40)
            )
            logo_label = ctk.CTkLabel(
                left_frame,
                image=bat_photo,
                text=""
            )
            logo_label.pack(side="left", padx=(0, 12))

        # Title
        self.title_label = ctk.CTkLabel(
            left_frame,
            text="KANTO ORDERS",
            font=get_font("heading", FONT_SIZES["title"], "bold"),
            text_color=COLORS["primary"]
        )
        self.title_label.pack(side="left")

        # Order count (right side)
        self.count_label = ctk.CTkLabel(
            self,
            text="Orders today: 0",
            font=get_font("body", FONT_SIZES["body"]),
            text_color=COLORS["text_dim"]
        )
        self.count_label.pack(side="right", padx=20, pady=15)

    def update_order_count(self, count: int) -> None:
        """Update the order count display."""
        self.order_count = count
        self.count_label.configure(text=f"Orders today: {count}")

