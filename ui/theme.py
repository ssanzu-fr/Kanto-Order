"""
Theme configuration - palette: e0fbfc / c2dfe3 / 9db4c0 / 5c6b73 / 253237 only
(plus two depth shades of the same hue). No other colors.
All UI styling comes from here.
"""

_C1 = "#e0fbfc"
_C2 = "#c2dfe3"
_C3 = "#9db4c0"
_C4 = "#5c6b73"
_C5 = "#253237"

_BG = "#1a2327"
_RAISED = "#2f3f45"

COLORS = {
    "background": _BG,
    "panel": _C5,
    "panel_hover": _RAISED,

    "primary": _C2,
    "primary_hover": _C1,
    "secondary": _C2,
    "secondary_hover": _C1,

    "text": _C1,
    "text_dim": _C3,

    "status_pending": _C1,
    "status_confirmed": _C2,
    "status_preparing": _C2,
    "status_ready": _C1,
    "status_completed": _C3,

    "border": _C4,
    "input_bg": _BG,
    "button_bg": _RAISED,
    "card_selected": _RAISED,

    "success": _C2,
    "error": _C1,
    "warning": _C1,
}

FONTS = {"heading": "Segoe UI", "body": "Segoe UI", "fallback": "Arial"}

FONT_SIZES = {"title": 26, "heading": 18, "subheading": 15, "body": 15, "small": 13}

SPACING = {"xs": 4, "sm": 8, "md": 16, "lg": 24, "xl": 32}

SIZES = {"button_height": 40, "input_height": 40, "corner_radius": 12}
