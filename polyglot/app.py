import customtkinter as ctk

from pathlib import Path
from polyglot.controllers.user_controller import UserController
from polyglot.controllers.vocabulary_controller import VocabularyController
from polyglot.views.onboarding_view import OnboardingView
from polyglot.views.menu_view import MenuView
from polyglot.views.flashcard_view import FlashcardView
from polyglot.views.test_view import TestView
from polyglot.views.sentence_test_view import SentenceTestView
from polyglot.views.sentence_translation_view import SentenceTranslationView
from polyglot.views.progress_view import ProgressView
from polyglot.views.settings_view import SettingsView
from polyglot.views.add_word_view import AddWordView

from dotenv import load_dotenv

load_dotenv()


class PolyglotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Polyglot - Language Learning")
        self.geometry("1024x768")

        # Set minimum size to ensure UI elements are visible
        self.minsize(900, 700)

        # Set the theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Initialize controllers
        self.user_controller = UserController()
        self.vocabulary_controller = VocabularyController(self.user_controller)

        # Initialize views dictionary
        self.views = {}
        self.current_view = None

        # Create data directory if it doesn't exist
        self.data_dir = Path.home() / ".polyglot"
        self.data_dir.mkdir(exist_ok=True)

        self.initialize_app()

    def initialize_app(self):
        """Initialize the application based on user data existence"""
        if not self.user_controller.user_exists():
            self.show_view("onboarding")
        else:
            # Generate new words for today
            self.generate_daily_words()
            self.show_view("menu")

    def generate_daily_words(self):
        """Generate new words for today's learning session if needed"""
        # Check if we need new words
        if self.vocabulary_controller.needs_new_words(min_unpracticed=5):
            settings = self.user_controller.get_settings()

            new_words = self.vocabulary_controller.generate_words(
                native_lang=settings["native_language"],
                target_lang=settings["target_language"],
                level=settings["level"],
                topics=settings["topics"],
                include_phrases=settings["include_phrases"],
            )

            self.vocabulary_controller.add_words(new_words)

    def show_view(self, view_type: str):
        """Show a specific view"""
        # Hide current view if exists
        if self.current_view:
            self.current_view.pack_forget()

        if view_type not in self.views:
            # Create view if it doesn't exist yet
            if view_type == "onboarding":
                self.views[view_type] = OnboardingView(
                    self, self.user_controller, lambda: self.show_view("menu")
                )
            elif view_type == "menu":
                self.views[view_type] = MenuView(
                    self,
                    self.vocabulary_controller,
                    lambda: self.show_view("flashcard"),  # daily_words_callback
                    lambda: self.show_view("flashcard"),  # exercise_callback
                    lambda: self.show_view("test"),  # word_test_callback
                    lambda: self.show_view("sentence_test"),
                    lambda: self.show_view("sentence_translation"),
                    lambda: self.show_view("progress"),
                    lambda: self.show_view("add_word"),
                    lambda: self.show_view("settings"),
                )
            elif view_type == "flashcard":
                self.views[view_type] = FlashcardView(
                    self,
                    self.vocabulary_controller,
                    lambda: self.show_view("test"),
                    on_menu_click=lambda: self.show_view("menu"),
                )
            elif view_type == "test":
                self.views[view_type] = TestView(
                    self,
                    self.vocabulary_controller,
                    lambda: self.show_view("sentence_test"),
                    on_menu_click=lambda: self.show_view("menu"),
                )
            elif view_type == "sentence_test":
                self.views[view_type] = SentenceTestView(
                    self,
                    self.vocabulary_controller,
                    lambda: self.show_view("sentence_translation"),
                    on_menu_click=lambda: self.show_view("menu"),
                )
            elif view_type == "sentence_translation":
                self.views[view_type] = SentenceTranslationView(
                    self,
                    self.vocabulary_controller,
                    lambda: self.show_view("progress"),
                    on_menu_click=lambda: self.show_view("menu"),
                )
            elif view_type == "progress":
                self.views[view_type] = ProgressView(
                    self,
                    self.vocabulary_controller,
                    lambda: self.show_view("menu"),
                    on_menu_click=lambda: self.show_view("menu"),
                )
            elif view_type == "add_word":
                self.views[view_type] = AddWordView(
                    self,
                    self.vocabulary_controller,
                    lambda: self.show_view("menu"),
                    on_menu_click=lambda: self.show_view("menu"),
                )
            elif view_type == "settings":
                self.views[view_type] = SettingsView(
                    self,
                    self.user_controller,
                    lambda: self.show_view("menu"),
                    on_menu_click=lambda: self.show_view("menu"),
                )

        self.current_view = self.views[view_type]
        self.current_view.pack(fill="both", expand=True)


def main():
    app = PolyglotApp()
    app.mainloop()


if __name__ == "__main__":
    main()
