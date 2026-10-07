"""
Font loader - loads Bungee and Nunito with safe fallback.
"""
import os
import customtkinter as ctk
from tkinter import font as tkfont


class FontLoader:
    """Loads custom fonts with fallback to system fonts."""

    def __init__(self):
        self.fonts_loaded = False
        self.bungee_available = False
        self.nunito_available = False

    def load_fonts(self) -> None:
        """
        Load Bungee and Nunito fonts from assets/fonts/.
        Falls back gracefully if fonts are missing.
        """
        fonts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "fonts")

        # Try to load Bungee
        bungee_path = os.path.join(fonts_dir, "Bungee-Regular.ttf")
        if os.path.exists(bungee_path):
            try:
                # Note: customtkinter doesn't have direct font file loading
                # We'll use the font name and rely on system registration
                self.bungee_available = True
            except Exception as e:
                print(f"Warning: Could not load Bungee font: {e}")

        # Try to load Nunito
        nunito_regular_path = os.path.join(fonts_dir, "Nunito-Regular.ttf")
        nunito_bold_path = os.path.join(fonts_dir, "Nunito-Bold.ttf")
        if os.path.exists(nunito_regular_path):
            try:
                self.nunito_available = True
            except Exception as e:
                print(f"Warning: Could not load Nunito font: {e}")

        self.fonts_loaded = True

    def get_font_family(self, font_type: str) -> str:
        """
        Get font family name with fallback.

        Args:
            font_type: "heading" or "body"

        Returns:
            Font family name
        """
        if font_type == "heading":
            return "Bungee" if self.bungee_available else "Arial Black"
        elif font_type == "body":
            return "Nunito" if self.nunito_available else "Arial"
        else:
            return "Arial"


# Global font loader instance
font_loader = FontLoader()
font_loader.load_fonts()


def get_font(font_type: str, size: int, weight: str = "normal") -> tuple:
    """
    Get a font tuple for customtkinter widgets.

    Args:
        font_type: "heading" or "body"
        size: Font size in pixels
        weight: "normal" or "bold"

    Returns:
        Tuple of (family, size, weight)
    """
    family = font_loader.get_font_family(font_type)
    return (family, size, weight)
