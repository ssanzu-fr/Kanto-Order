"""
Kanto Orders - Main entry point
A Filipino food stall ordering system for business process management.
"""
from ui.app import App


def main():
    """Launch the application."""
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
