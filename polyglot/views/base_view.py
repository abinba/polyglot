import customtkinter as ctk
from typing import Callable, Optional


class BaseView(ctk.CTkFrame):
    """Base view class with common functionality for all views."""

    def __init__(self, parent):
        super().__init__(parent)
        self.back_to_menu_button = None

    def add_back_to_menu_button(self, on_menu_click: Callable):
        """Add a back to main menu button to the top-right corner of the view."""
        self.back_to_menu_button = ctk.CTkButton(
            self, text="Back to Menu", width=120, height=30, command=on_menu_click
        )
        # Place in top-right corner
        self.back_to_menu_button.place(relx=0.95, rely=0.05, anchor="e")

    def remove_back_to_menu_button(self):
        """Remove the back to menu button if it exists."""
        if self.back_to_menu_button:
            self.back_to_menu_button.place_forget()
            self.back_to_menu_button = None
