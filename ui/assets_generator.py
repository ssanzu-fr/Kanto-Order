"""
Asset generator - creates bat logo and other visual assets.
"""
from PIL import Image, ImageDraw
import os


def create_bat_logo(size: int = 64, color: str = "#ffd700") -> Image.Image:
    """
    Create a simple bat silhouette logo.

    Args:
        size: Size of the square image
        color: Hex color for the bat

    Returns:
        PIL Image with transparent background
    """
    # Create transparent image
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Convert hex to RGB
    color_rgb = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

    # Draw bat silhouette using polygons
    # Body (center oval)
    body_x = size // 2
    body_y = size // 2
    body_w = size // 8
    body_h = size // 4
    draw.ellipse([
        body_x - body_w, body_y - body_h // 2,
        body_x + body_w, body_y + body_h // 2 + body_h // 4
    ], fill=color_rgb + (255,))

    # Head (small circle on top)
    head_r = size // 10
    draw.ellipse([
        body_x - head_r, body_y - body_h // 2 - head_r,
        body_x + head_r, body_y - body_h // 2 + head_r
    ], fill=color_rgb + (255,))

    # Left wing
    left_wing = [
        (body_x - body_w, body_y),  # Connection to body
        (size // 8, body_y - size // 6),  # Top curve
        (size // 16, body_y + size // 8),  # Bottom point
    ]
    draw.polygon(left_wing, fill=color_rgb + (255,))

    # Right wing (mirror)
    right_wing = [
        (body_x + body_w, body_y),  # Connection to body
        (size - size // 8, body_y - size // 6),  # Top curve
        (size - size // 16, body_y + size // 8),  # Bottom point
    ]
    draw.polygon(right_wing, fill=color_rgb + (255,))

    # Ears
    ear_size = size // 12
    # Left ear
    draw.polygon([
        (body_x - head_r // 2, body_y - body_h // 2 - head_r),
        (body_x - head_r, body_y - body_h // 2 - head_r - ear_size),
        (body_x, body_y - body_h // 2 - head_r)
    ], fill=color_rgb + (255,))
    # Right ear
    draw.polygon([
        (body_x + head_r // 2, body_y - body_h // 2 - head_r),
        (body_x + head_r, body_y - body_h // 2 - head_r - ear_size),
        (body_x, body_y - body_h // 2 - head_r)
    ], fill=color_rgb + (255,))

    return img


def save_bat_logo(output_path: str, size: int = 64, color: str = "#ffd700") -> None:
    """Save bat logo to file."""
    img = create_bat_logo(size, color)

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    img.save(output_path, 'PNG')


def create_small_bat(size: int = 24, color: str = "#ffd700") -> Image.Image:
    """Create a smaller bat accent for UI elements."""
    return create_bat_logo(size, color)


if __name__ == "__main__":
    import sys
    import io
    # Fix Windows console encoding
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # Generate bat assets
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "images")

    # Main logo
    save_bat_logo(os.path.join(assets_dir, "bat_logo.png"), size=64, color="#ffd700")

    # Small accent
    save_bat_logo(os.path.join(assets_dir, "bat_small.png"), size=24, color="#ffd700")

    print("Bat assets created:")
    print(f"  - {os.path.join(assets_dir, 'bat_logo.png')}")
    print(f"  - {os.path.join(assets_dir, 'bat_small.png')}")
