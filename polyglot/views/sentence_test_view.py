import customtkinter as ctk
from typing import Callable
from polyglot.controllers.vocabulary_controller import VocabularyController


class SentenceTestView(ctk.CTkFrame):
    def __init__(
        self, parent, vocab_controller: VocabularyController, on_complete: Callable
    ):
        super().__init__(parent)
        self.vocab_controller = vocab_controller
        self.on_complete = on_complete

        self.current_word_idx = 0
        self.test_words = None
        self.correct_answers = 0
        self.answer_checked = False
        self.selected_option = None

        self.setup_ui()
        self.load_test_words()

        # Bind space key to check/next
        self.master.bind("<space>", lambda e: self.handle_space())

    def setup_ui(self):
        """Set up the main UI components"""
        # Title
        self.title = ctk.CTkLabel(
            self, text="Sentence Practice", font=("Helvetica", 24, "bold")
        )
        self.title.pack(pady=20)

        # Question frame
        self.question_frame = ctk.CTkFrame(self)
        self.question_frame.pack(pady=20, padx=40, fill="both", expand=True)

        # Sentence label
        self.sentence_label = ctk.CTkLabel(
            self.question_frame, text="", font=("Helvetica", 16), wraplength=500
        )
        self.sentence_label.pack(pady=20)

        # Options frame
        self.options_frame = ctk.CTkFrame(self.question_frame)
        self.options_frame.pack(pady=10, fill="x", padx=20)

        # Create option buttons
        self.option_buttons = []
        for i in range(4):
            btn = ctk.CTkButton(
                self.options_frame,
                text="",
                command=lambda idx=i: self.select_option(idx),
                width=200,
                height=40,
            )
            btn.pack(pady=5, fill="x")
            self.option_buttons.append(btn)

        # Ensure we have all 4 buttons
        assert len(self.option_buttons) == 4, "Not all option buttons were created"

        # Translation label (hidden initially)
        self.translation_label = ctk.CTkLabel(
            self.question_frame, text="", font=("Helvetica", 16), wraplength=500
        )
        self.translation_label.pack(pady=10)

        # Feedback label
        self.feedback_label = ctk.CTkLabel(
            self.question_frame, text="", font=("Helvetica", 16)
        )
        self.feedback_label.pack(pady=10)

        # Instructions label
        self.instructions_label = ctk.CTkLabel(
            self,
            text="Click an option to answer, press SPACE to continue",
            font=("Helvetica", 14),
        )
        self.instructions_label.pack(pady=10)

        # Progress label
        self.progress_label = ctk.CTkLabel(self, text="", font=("Helvetica", 14))
        self.progress_label.pack(pady=10)

    def load_test_words(self):
        """Load words for the sentence test session"""
        self.test_words = self.vocab_controller.get_test_words(
            count=self.vocab_controller.user_controller.test_word_count
        )
        if not self.test_words.empty:
            self.show_question(0)
        else:
            self.show_no_words_message()

    def show_question(self, idx: int):
        """Display the sentence question at the specified index"""
        if idx < len(self.test_words):
            word = self.test_words.iloc[idx]
            options = word["options"]

            # Ensure we have exactly 4 options
            if not isinstance(options, list) or len(options) != 4:
                raise ValueError(f"Word {word['word']} does not have exactly 4 options")

            # Clear previous state
            self.feedback_label.configure(text="")
            self.translation_label.configure(text="")
            self.answer_checked = False
            self.selected_option = None

            # Show sentence
            self.sentence_label.configure(text=word["sentence_to_fill"])

            # Update options
            for i, option in enumerate(options):
                self.option_buttons[i].configure(
                    text=option, state="normal", fg_color=("#2B2B2B", "#242424")
                )

            # Update progress
            self.progress_label.configure(
                text=f"Question {idx + 1} of {len(self.test_words)}"
            )

    def handle_space(self):
        """Handle space key press - either check answer or advance to next question"""
        if not self.answer_checked:
            self.check_answer()
        else:
            self.next_question()

    def select_option(self, option_idx: int):
        """Handle option selection"""
        if not self.answer_checked:
            self.selected_option = option_idx
            self.check_answer()

    def check_answer(self):
        """Check the user's answer"""
        if (
            self.current_word_idx < len(self.test_words)
            and self.selected_option is not None
        ):
            word = self.test_words.iloc[self.current_word_idx]
            selected_answer = word["options"][self.selected_option]

            is_correct = selected_answer == word["correct_answer"]

            # Update word statistics
            self.vocab_controller.update_word_stats(word["word"], is_correct)

            # Update UI
            if is_correct:
                self.feedback_label.configure(
                    text="Correct! ✓\nPress SPACE to continue", text_color="green"
                )
                self.correct_answers += 1
                self.option_buttons[self.selected_option].configure(fg_color="green")
            else:
                self.feedback_label.configure(
                    text=f"Incorrect. The correct answer is: {word['correct_answer']} ✗\nPress SPACE to continue",
                    text_color="red",
                )
                self.option_buttons[self.selected_option].configure(fg_color="red")
                # Highlight correct answer
                correct_idx = word["options"].index(word["correct_answer"])
                self.option_buttons[correct_idx].configure(fg_color="green")

            # Show translation
            self.translation_label.configure(
                text=f"Translation: {word['sentence_to_fill_translation']}"
            )

            # Disable options
            for btn in self.option_buttons:
                btn.configure(state="disabled")

            self.answer_checked = True

    def next_question(self):
        """Move to the next question or complete the test"""
        self.current_word_idx += 1
        if self.current_word_idx < len(self.test_words):
            self.show_question(self.current_word_idx)
        else:
            self.show_completion()

    def show_no_words_message(self):
        """Show message when no words are available for testing"""
        # Clear question frame
        for widget in self.question_frame.winfo_children():
            widget.destroy()

        # Show message
        message_label = ctk.CTkLabel(
            self.question_frame,
            text="No words available for testing yet!\n\n"
            "Please review some words in the flashcard view first.",
            font=("Helvetica", 20),
        )
        message_label.pack(pady=20)

        # Clear instructions and progress
        self.instructions_label.configure(text="")
        self.progress_label.configure(text="")

        # Add button to go back to flashcards
        back_btn = ctk.CTkButton(
            self.question_frame, text="Go to Flashcards", command=self.on_complete
        )
        back_btn.pack(pady=20)

    def show_completion(self):
        """Show completion message and final score"""
        # Clear question frame
        for widget in self.question_frame.winfo_children():
            widget.destroy()

        # Calculate score
        total_questions = len(self.test_words)
        score_percentage = (
            self.correct_answers / total_questions * 100 if total_questions > 0 else 0
        )

        # Show completion message
        completion_label = ctk.CTkLabel(
            self.question_frame,
            text=f"Sentence Practice Complete!\n\nScore: {self.correct_answers}/{total_questions}"
            f" ({score_percentage:.1f}%)\n\nGreat job practicing with sentences!",
            font=("Helvetica", 20),
        )
        completion_label.pack(pady=20)

        # Clear instructions
        self.instructions_label.configure(text="")

        # Update progress label
        self.progress_label.configure(text="")

        # Move to progress view
        self.after(2000, self.on_complete)
