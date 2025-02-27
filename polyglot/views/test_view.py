import customtkinter as ctk
from typing import Callable, List
import random
from polyglot.controllers.vocabulary_controller import VocabularyController
from polyglot.views.base_view import BaseView


class TestView(BaseView):
    def __init__(
        self,
        parent,
        vocab_controller: VocabularyController,
        on_complete: Callable,
        on_menu_click: Callable = None,
    ):
        super().__init__(parent)
        self.vocab_controller = vocab_controller
        self.on_complete = on_complete
        self.on_menu_click = on_menu_click

        self.current_question = 0
        self.test_words = None
        self.current_options = []
        self.correct_answers = 0
        self.answer_checked = False

        self.setup_ui()
        self.load_test_words()

        # Add back to menu button if callback provided
        if self.on_menu_click:
            self.add_back_to_menu_button(self.on_menu_click)

        # Bind space key to check/next
        self.master.bind("<space>", lambda e: self.handle_space())

    def setup_ui(self):
        """Set up the main UI components"""
        # Title
        self.title = ctk.CTkLabel(
            self, text="Translation Test", font=("Helvetica", 24, "bold")
        )
        self.title.pack(pady=20)

        # Question frame
        self.question_frame = ctk.CTkFrame(self)
        self.question_frame.pack(pady=20, padx=40, fill="both", expand=True)

        # Word label
        self.word_label = ctk.CTkLabel(
            self.question_frame, text="", font=("Helvetica", 20)
        )
        self.word_label.pack(pady=20)

        # Answer entry
        self.answer_entry = ctk.CTkEntry(
            self.question_frame, width=300, placeholder_text="Type your answer here..."
        )
        self.answer_entry.pack(pady=10)

        # Options frame for multiple choice
        self.options_frame = ctk.CTkFrame(self.question_frame)
        self.options_frame.pack(pady=20, fill="x")

        # Feedback label
        self.feedback_label = ctk.CTkLabel(
            self.question_frame, text="", font=("Helvetica", 16)
        )
        self.feedback_label.pack(pady=10)

        # Instructions label
        self.instructions_label = ctk.CTkLabel(
            self, text="Press SPACE to check answer and advance", font=("Helvetica", 14)
        )
        self.instructions_label.pack(pady=10)

        # Progress label
        self.progress_label = ctk.CTkLabel(self, text="", font=("Helvetica", 14))
        self.progress_label.pack(pady=10)

        # Bind return key to check answer
        self.answer_entry.bind("<Return>", lambda e: self.handle_space())

    def load_test_words(self):
        """Load words for the test session"""
        self.test_words = self.vocab_controller.get_test_words(
            count=self.vocab_controller.user_controller.test_word_count
        )
        if not self.test_words.empty:
            self.show_question(0)
        else:
            self.show_completion()

    def show_question(self, idx: int):
        """Display the question at the specified index"""
        if idx < len(self.test_words):
            word = self.test_words.iloc[idx]

            # Clear previous state
            self.answer_entry.delete(0, "end")
            self.feedback_label.configure(text="")
            self.answer_entry.configure(state="normal")
            self.answer_checked = False

            # Show word
            self.word_label.configure(text=word["translation"])

            # Generate options for multiple choice
            self.generate_options(word)

            # Update progress
            self.progress_label.configure(
                text=f"Question {idx + 1} of {len(self.test_words)}"
            )

    def generate_options(self, current_word):
        """Generate multiple choice options"""
        # Clear previous options
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        # Get three random words as distractors
        other_words = self.vocab_controller.vocabulary[
            self.vocab_controller.vocabulary["word"] != current_word["word"]
        ]["word"].tolist()

        options = random.sample(other_words, min(3, len(other_words)))
        options.append(current_word["word"])
        random.shuffle(options)

        self.current_options = options

        # Create option buttons
        for i, option in enumerate(options):
            btn = ctk.CTkButton(
                self.options_frame,
                text=option,
                command=lambda o=option: self.select_option(o),
            )
            btn.pack(pady=5)

    def select_option(self, option: str):
        """Handle option selection"""
        self.answer_entry.delete(0, "end")
        self.answer_entry.insert(0, option)

    def handle_space(self):
        """Handle space key press - either check answer or advance to next question"""
        if not self.answer_checked:
            self.check_answer()
        else:
            self.next_question()

    def check_answer(self):
        """Check the user's answer"""
        if self.current_question < len(self.test_words):
            word = self.test_words.iloc[self.current_question]
            user_answer = self.answer_entry.get().strip().lower()
            correct_answer = word["word"].lower()

            is_correct = user_answer == correct_answer

            # Update word statistics
            self.vocab_controller.update_word_stats(word["word"], is_correct)

            # Update UI
            if is_correct:
                self.feedback_label.configure(
                    text="Correct! \nPress SPACE to continue", text_color="green"
                )
                self.correct_answers += 1
            else:
                self.feedback_label.configure(
                    text=f"Incorrect. The correct answer is: {word['word']} \nPress SPACE to continue",
                    text_color="red",
                )

            # Disable input
            self.answer_entry.configure(state="disabled")
            self.answer_checked = True

    def next_question(self):
        """Move to the next question or complete the test"""
        self.current_question += 1
        if self.current_question < len(self.test_words):
            # Clear input field before showing next question
            self.answer_entry.delete(0, "end")
            self.show_question(self.current_question)
        else:
            self.show_completion()

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
            text=f"Test Complete!\n\nScore: {self.correct_answers}/{total_questions}"
            f" ({score_percentage:.1f}%)\n\nNow let's practice using these words in sentences!",
            font=("Helvetica", 20),
        )
        completion_label.pack(pady=20)

        # Clear instructions
        self.instructions_label.configure(text="")

        # Update progress label
        self.progress_label.configure(text="")

        # Move to sentence test
        self.after(2000, self.on_complete)
