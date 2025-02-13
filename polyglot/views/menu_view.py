import customtkinter as ctk
from typing import Callable, Dict
from polyglot.controllers.vocabulary_controller import VocabularyController
from polyglot.controllers.user_controller import UserController


class MenuView(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        vocab_controller: VocabularyController,
        user_controller: UserController,
        view_callbacks: Dict[str, Callable],
    ):
        super().__init__(parent)
        self.vocab_controller = vocab_controller
        self.user_controller = user_controller
        self.view_callbacks = view_callbacks

        self.setup_ui()
        self.update_word_count()

    def setup_ui(self):
        """Set up the main UI components"""
        # Welcome section
        self.welcome_frame = ctk.CTkFrame(self)
        self.welcome_frame.pack(pady=20, padx=40, fill="x")

        self.title = ctk.CTkLabel(
            self.welcome_frame,
            text="Welcome to Polyglot",
            font=("Helvetica", 28, "bold"),
        )
        self.title.pack(pady=10)

        self.word_count_label = ctk.CTkLabel(
            self.welcome_frame, text="", font=("Helvetica", 16)
        )
        self.word_count_label.pack(pady=5)

        # Menu sections frame
        self.sections_frame = ctk.CTkFrame(self)
        self.sections_frame.pack(pady=20, padx=40, fill="both", expand=True)

        # Practice section
        self.practice_label = ctk.CTkLabel(
            self.sections_frame, text="Practice", font=("Helvetica", 20, "bold")
        )
        self.practice_label.pack(pady=(20, 10), padx=20, anchor="w")

        self.practice_frame = ctk.CTkFrame(self.sections_frame, fg_color="transparent")
        self.practice_frame.pack(fill="x", padx=20)

        # Words of the day
        self.words_btn = self._create_menu_button(
            self.practice_frame,
            "📚 Words of the Day",
            "Review today's vocabulary",
            lambda: self.view_callbacks["daily_words"](),
        )

        # Exercise session
        self.exercise_btn = self._create_menu_button(
            self.practice_frame,
            "🎯 Exercise Session",
            "Complete practice session",
            lambda: self.view_callbacks["exercise"](),
        )

        # Tests section
        self.tests_label = ctk.CTkLabel(
            self.sections_frame, text="Tests", font=("Helvetica", 20, "bold")
        )
        self.tests_label.pack(pady=(20, 10), padx=20, anchor="w")

        self.tests_frame = ctk.CTkFrame(self.sections_frame, fg_color="transparent")
        self.tests_frame.pack(fill="x", padx=20)

        # Word translation test
        self.word_test_btn = self._create_menu_button(
            self.tests_frame,
            "🔤 Word Translation",
            "Test word translations",
            lambda: self.view_callbacks["word_test"](),
        )

        # Sentence filling test
        self.sentence_test_btn = self._create_menu_button(
            self.tests_frame,
            "📝 Sentence Filling",
            "Practice with sentences",
            lambda: self.view_callbacks["sentence_test"](),
        )

        # Tools section
        self.tools_label = ctk.CTkLabel(
            self.sections_frame, text="Tools", font=("Helvetica", 20, "bold")
        )
        self.tools_label.pack(pady=(20, 10), padx=20, anchor="w")

        self.tools_frame = ctk.CTkFrame(self.sections_frame, fg_color="transparent")
        self.tools_frame.pack(fill="x", padx=20)

        # Progress view
        self.progress_btn = self._create_menu_button(
            self.tools_frame,
            "📊 Progress",
            "Track your learning",
            lambda: self.view_callbacks["progress"](),
        )

        # Add word
        self.add_word_btn = self._create_menu_button(
            self.tools_frame,
            "➕ Add Word",
            "Add custom vocabulary",
            lambda: self.view_callbacks["add_word"](),
        )

        # Settings
        self.settings_btn = self._create_menu_button(
            self.tools_frame,
            "⚙️ Settings",
            "Configure app settings",
            lambda: self.view_callbacks["settings"](),
        )

    def _create_menu_button(self, parent, text, description, command):
        """Create a menu button with icon and description"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(pady=5, fill="x")

        button = ctk.CTkButton(
            frame,
            text=text,
            command=command,
            height=40,
            anchor="w",
            font=("Helvetica", 16),
        )
        button.pack(side="left", padx=(0, 10), fill="x", expand=True)

        desc_label = ctk.CTkLabel(
            frame, text=description, font=("Helvetica", 12), text_color="gray"
        )
        desc_label.pack(side="left", padx=10)

        return button

    def update_word_count(self):
        """Update the word count display"""
        vocab_df = self.vocab_controller.vocabulary
        total_words = len(vocab_df)

        # Count words that have been practiced at least 7 times with 75% success rate
        learned_words = len(
            vocab_df[
                (vocab_df["times_practiced"] >= 7)
                & (vocab_df["correct_answers"] / vocab_df["times_practiced"] >= 0.75)
            ]
        )

        self.word_count_label.configure(
            text=f"Total Words: {total_words} | Words Learnt: {learned_words}"
        )
