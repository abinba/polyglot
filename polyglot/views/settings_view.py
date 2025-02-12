import customtkinter as ctk
from typing import Callable
from polyglot.controllers.user_controller import UserController


class SettingsView(ctk.CTkFrame):
    def __init__(self, parent, user_controller: UserController, on_complete: Callable):
        super().__init__(parent)
        self.user_controller = user_controller
        self.on_complete = on_complete

        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        """Set up the main UI components"""
        # Title
        self.title = ctk.CTkLabel(self, text="Settings", font=("Helvetica", 24, "bold"))
        self.title.pack(pady=20)

        # Settings frame
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.pack(pady=20, padx=40, fill="both", expand=True)

        # Words per day setting
        self.words_per_day_frame = ctk.CTkFrame(self.settings_frame)
        self.words_per_day_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(
            self.words_per_day_frame, text="Words per day:", font=("Helvetica", 16)
        ).pack(side="left", padx=10)

        self.words_per_day_var = ctk.StringVar()
        self.words_per_day_entry = ctk.CTkEntry(
            self.words_per_day_frame, width=100, textvariable=self.words_per_day_var
        )
        self.words_per_day_entry.pack(side="right", padx=10)

        # Flashcard delay setting
        self.flashcard_delay_frame = ctk.CTkFrame(self.settings_frame)
        self.flashcard_delay_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(
            self.flashcard_delay_frame,
            text="Flashcard delay (seconds):",
            font=("Helvetica", 16),
        ).pack(side="left", padx=10)

        self.flashcard_delay_var = ctk.StringVar()
        self.flashcard_delay_entry = ctk.CTkEntry(
            self.flashcard_delay_frame, width=100, textvariable=self.flashcard_delay_var
        )
        self.flashcard_delay_entry.pack(side="right", padx=10)

        # Test word count setting
        self.test_word_count_frame = ctk.CTkFrame(self.settings_frame)
        self.test_word_count_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(
            self.test_word_count_frame, text="Words per test:", font=("Helvetica", 16)
        ).pack(side="left", padx=10)

        self.test_word_count_var = ctk.StringVar()
        self.test_word_count_entry = ctk.CTkEntry(
            self.test_word_count_frame, width=100, textvariable=self.test_word_count_var
        )
        self.test_word_count_entry.pack(side="right", padx=10)

        # Navigation frame
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.pack(pady=20, fill="x")

        # Save button
        self.save_btn = ctk.CTkButton(
            self.nav_frame, text="Save", command=self.save_settings
        )
        self.save_btn.pack(side="right", padx=20)

        # Cancel button
        self.cancel_btn = ctk.CTkButton(
            self.nav_frame, text="Cancel", command=self.on_complete
        )
        self.cancel_btn.pack(side="left", padx=20)

    def load_settings(self):
        """Load current settings"""
        settings = self.user_controller.get_settings()

        self.words_per_day_var.set(str(settings.get("words_per_day", 5)))
        self.flashcard_delay_var.set(str(settings.get("flashcard_delay", 5)))
        self.test_word_count_var.set(str(settings.get("test_word_count", 10)))

    def save_settings(self):
        """Save settings and return to previous view"""
        try:
            # Validate and update settings
            words_per_day = max(1, min(50, int(self.words_per_day_var.get())))
            flashcard_delay = max(1, min(30, int(self.flashcard_delay_var.get())))
            test_word_count = max(5, min(50, int(self.test_word_count_var.get())))

            self.user_controller.update_settings(
                {
                    "words_per_day": words_per_day,
                    "flashcard_delay": flashcard_delay,
                    "test_word_count": test_word_count,
                }
            )

            self.on_complete()

        except ValueError:
            # Show error message if input is invalid
            error_label = ctk.CTkLabel(
                self.settings_frame,
                text="Please enter valid numbers",
                text_color="red",
                font=("Helvetica", 14),
            )
            error_label.pack(pady=10)
            self.after(3000, error_label.destroy)
