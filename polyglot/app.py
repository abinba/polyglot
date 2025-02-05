import customtkinter as ctk

from pathlib import Path
from polyglot.controllers.user_controller import UserController
from polyglot.controllers.vocabulary_controller import VocabularyController
from polyglot.views.onboarding_view import OnboardingView
from polyglot.views.flashcard_view import FlashcardView
from polyglot.views.test_view import TestView
from polyglot.views.sentence_test_view import SentenceTestView
from polyglot.views.progress_view import ProgressView
from polyglot.views.settings_view import SettingsView

from dotenv import load_dotenv
load_dotenv()


class PolyglotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Polyglot - Language Learning")
        self.geometry("900x600")
        
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
            self.show_onboarding()
        else:
            # Generate new words for today
            self.generate_daily_words()
            self.show_flashcards()
    
    def generate_daily_words(self):
        """Generate new words for today's learning session if needed"""
        # Check if we need new words
        if self.vocabulary_controller.needs_new_words(min_unpracticed=5):
            settings = self.user_controller.get_settings()
            
            new_words = self.vocabulary_controller.generate_words(
                native_lang=settings['native_language'],
                target_lang=settings['target_language'],
                level=settings['level'],
                topics=settings['topics'],
                include_phrases=settings['include_phrases']
            )
            
            self.vocabulary_controller.add_words(new_words)
    
    def show_onboarding(self):
        """Show the onboarding view for new users"""
        if 'onboarding' not in self.views:
            self.views['onboarding'] = OnboardingView(
                self,
                self.user_controller,
                self.vocabulary_controller,
                self.show_flashcards
            )
        self._switch_view('onboarding')
    
    def show_flashcards(self):
        """Show the flashcard learning view"""
        if 'flashcards' not in self.views:
            self.views['flashcards'] = FlashcardView(
                self,
                self.vocabulary_controller,
                self.show_test
            )
        self._switch_view('flashcards')
    
    def show_test(self):
        """Show the translation test view"""
        if 'test' not in self.views:
            self.views['test'] = TestView(
                self,
                self.vocabulary_controller,
                self.show_sentence_test
            )
        self._switch_view('test')
    
    def show_sentence_test(self):
        """Show the sentence test view"""
        if 'sentence_test' not in self.views:
            self.views['sentence_test'] = SentenceTestView(
                self,
                self.vocabulary_controller,
                self.show_progress
            )
        self._switch_view('sentence_test')
    
    def show_progress(self):
        """Show the progress view"""
        if 'progress' not in self.views:
            self.views['progress'] = ProgressView(
                self,
                self.vocabulary_controller,
                self.show_flashcards
            )
        self._switch_view('progress')
    
    def show_settings(self):
        """Show the settings view"""
        if 'settings' not in self.views:
            self.views['settings'] = SettingsView(
                self,
                self.user_controller,
                self.show_flashcards
            )
        self._switch_view('settings')
    
    def _switch_view(self, view_name):
        """Switch to the specified view"""
        if self.current_view:
            self.current_view.pack_forget()
        
        self.current_view = self.views[view_name]
        self.current_view.pack(fill="both", expand=True)

def main():
    app = PolyglotApp()
    app.mainloop()

if __name__ == "__main__":
    main()
