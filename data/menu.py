"""
Menu data - all available items organized by category.
"""
from models.menu_item import MenuItem


# All menu items
MENU_ITEMS = [
    # Rice and Soup
    MenuItem(id="lugaw", name="Lugaw", price=35, category="Rice and Soup"),
    MenuItem(id="goto", name="Goto", price=50, category="Rice and Soup"),
    MenuItem(id="mami", name="Mami", price=65, category="Rice and Soup"),
    MenuItem(id="pares", name="Pares", price=80, category="Rice and Soup"),
    MenuItem(id="chicken_meal", name="Chicken Meal", price=120, category="Rice and Soup"),

    # Street Food
    MenuItem(id="kwek_kwek", name="Kwek-kwek (5 pcs)", price=30, category="Street Food"),
    MenuItem(id="fishball", name="Fishball (10 pcs)", price=20, category="Street Food"),
    MenuItem(id="isaw", name="Isaw (2 sticks)", price=25, category="Street Food"),
    MenuItem(id="pagpag", name="Pagpag", price=45, category="Street Food"),

    # Drinks
    MenuItem(id="sago_gulaman", name="Sago't Gulaman", price=25, category="Drinks"),
    MenuItem(id="buko_juice", name="Buko Juice", price=35, category="Drinks"),
    MenuItem(id="iced_tea", name="Iced Tea", price=25, category="Drinks"),
]


def get_menu_by_category() -> dict:
    """Return menu items organized by category."""
    categories = {}
    for item in MENU_ITEMS:
        if item.category not in categories:
            categories[item.category] = []
        categories[item.category].append(item)
    return categories


def get_item_by_id(item_id: str) -> MenuItem:
    """Find a menu item by its ID."""
    for item in MENU_ITEMS:
        if item.id == item_id:
            return item
    return None
