"""
Theme configuration - minimal modern dark palette.

Palette: e0fbfc / c2dfe3 / 9db4c0 / 5c6b73 / 253237 only
(plus two depth shades of the same hue). No other colors.
All UI styling comes from here.
"""

# --- Core palette: your 5 colors + 2 depth shades of the same hue --------
_C1 = "#e0fbfc"          # lightest  - main text, highlights
_C2 = "#c2dfe3"          # accent
_C3 = "#9db4c0"          # secondary text
_C4 = "#5c6b73"          # borders
_C5 = "#253237"          # panels

_BG = "#1a2327"          # app background (darker than C5)
_RAISED = "#2f3f45"      # hover / buttons / selected (lighter than C5)

COLORS = {
    # Base
    "background": _BG,
    "panel": _C5,
    "panel_hover": _RAISED,

    # Accent (secondary kept as alias so no code breaks)
    "primary": _C2,
    "primary_hover": _C1,
    "secondary": _C2,
    "secondary_hover": _C1,

    # Text
    "text": _C1,
    "text_dim": _C3,

    # Status: brightest = needs action, dimmer = finished.
    # (Each badge also shows its text label, e.g. PAID / READY.)
    "status_pending": _C1,
    "status_confirmed": _C2,
    "status_preparing": _C2,
    "status_ready": _C1,
    "status_completed": _C3,

    # UI elements
    "border": _C4,
    "input_bg": _BG,
    "button_bg": _RAISED,
    "card_selected": _RAISED,

    # Semantic (same palette, no extra hues)
    "success": _C2,
    "error": _C1,
    "warning": _C1,
}

# FONTS
FONTS = {
    "heading": "Segoe UI",
    "body": "Segoe UI",
    "fallback": "Arial",
}

# FONT SIZES
FONT_SIZES = {
    "title": 26,
    "heading": 18,
    "subheading": 15,
    "body": 15,
    "small": 13,
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
    "corner_radius": 12,
}