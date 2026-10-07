"""
Theme configuration - Night market palette, fonts, and sizes.
All UI styling comes from here.
"""

# NIGHT MARKET PALETTE
COLORS = {
    # Base colors
    "background": "#0a0e1a",        # Deep night blue-black
    "panel": "#1a1f2e",             # Panel background with warm tint
    "panel_hover": "#252a3d",       # Panel hover state

    # Accent colors
    "primary": "#ffd700",           # Lantern yellow
    "primary_hover": "#ffed4e",     # Lighter yellow for hover
    "secondary": "#dc2626",         # Chili red
    "secondary_hover": "#ef4444",   # Lighter red for hover

    # Text colors
    "text": "#f5f1e8",              # Warm cream
    "text_dim": "#9ca3af",          # Dimmed text for labels

    # Status colors (for badges)
    "status_pending": "#d97706",    # Amber for pending payment
    "status_confirmed": "#2563eb",  # Blue for confirmed
    "status_preparing": "#7c3aed",  # Purple for preparing
    "status_ready": "#059669",      # Green for ready
    "status_completed": "#64748b",  # Slate gray for completed

    # UI elements
    "border": "#374151",            # Subtle borders
    "input_bg": "#111827",          # Input background
    "button_bg": "#1f2937",         # Button background
    "card_selected": "#252a3d",     # Selected card background

    # Semantic colors
    "success": "#10b981",           # Success green
    "error": "#ef4444",             # Error red
    "warning": "#f59e0b",           # Warning orange
}

# FONTS
FONTS = {
    "heading": "Bungee",            # Neon-sign feel for headers
    "body": "Nunito",               # Clean and readable for body text
    "fallback": "Arial",            # System fallback
}

# FONT SIZES
FONT_SIZES = {
    "title": 28,                    # Main app title
    "heading": 20,                  # Section headings
    "subheading": 16,               # Subsection headings
    "body": 14,                     # Regular text
    "small": 12,                    # Small labels and captions
}

# SPACING
SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 24,
    "xl": 32,
}

# SIZES
SIZES = {
    "button_height": 40,
    "input_height": 40,
    "corner_radius": 8,
}
