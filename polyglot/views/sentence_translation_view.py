import customtkinter as ctk
from typing import Callable
import pandas as pd
import threading
from polyglot.controllers.vocabulary_controller import VocabularyController
from datetime import datetime
from polyglot.views.base_view import BaseView


class SentenceTranslationView(BaseView):
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

        self.current_word_idx = 0
        self.test_words = None
        self.correct_answers = 0
        self.answer_checked = False
        self.is_checking = False  # Flag to track if we are in the middle of a check
        self.user_settings = self.vocab_controller.user_controller.get_settings()

        self.setup_ui()
        self.load_practice_sentences()

        # Bind return key to check/next
        self.master.bind("<Return>", lambda e: self.handle_enter())

        # Add back to menu button if callback provided
        if self.on_menu_click:
            self.add_back_to_menu_button(self.on_menu_click)

    def setup_ui(self):
        """Set up the main UI components"""
        # Title
        self.title = ctk.CTkLabel(
            self, text="Sentence Translation Practice", font=("Helvetica", 24, "bold")
        )
        self.title.pack(pady=20)

        # Question frame
        self.question_frame = ctk.CTkFrame(self)
        self.question_frame.pack(pady=20, padx=40, fill="both", expand=True)

        # Native sentence label
        self.native_sentence_label = ctk.CTkLabel(
            self.question_frame, text="", font=("Helvetica", 16), wraplength=600
        )
        self.native_sentence_label.pack(pady=20)

        # Translation instruction
        self.instruction_label = ctk.CTkLabel(
            self.question_frame,
            text=f"Translate this sentence to {self.user_settings['target_language']}:",
            font=("Helvetica", 14),
        )
        self.instruction_label.pack(pady=5)

        # Translation entry
        self.translation_entry = ctk.CTkTextbox(
            self.question_frame, height=100, width=600
        )
        self.translation_entry.pack(pady=10, padx=20, fill="x")

        # Button frame for check and don't know buttons
        self.button_frame = ctk.CTkFrame(self.question_frame, fg_color="transparent")
        self.button_frame.pack(pady=5)

        # Check button
        self.check_button = ctk.CTkButton(
            self.button_frame, text="Check Translation", command=self.check_answer
        )
        self.check_button.pack(side="left", padx=10)

        # I don't know button
        self.dont_know_button = ctk.CTkButton(
            self.button_frame,
            text="I Don't Know",
            command=self.show_correct_translation,
            fg_color="#FF9060",  # Distinct color to differentiate from other buttons
            hover_color="#E86C3D",
        )
        self.dont_know_button.pack(side="left", padx=10)

        # Feedback label
        self.feedback_label = ctk.CTkLabel(
            self.question_frame, text="", font=("Helvetica", 14), wraplength=600
        )
        self.feedback_label.pack(pady=10)

        # Next button (initially hidden)
        self.next_button = ctk.CTkButton(
            self.question_frame, text="Next Sentence", command=self.next_question
        )
        self.next_button.pack(pady=10)
        self.next_button.pack_forget()  # Hide initially

        # Loading indicator
        self.loading_label = ctk.CTkLabel(
            self.question_frame,
            text="Checking your translation...",
            font=("Helvetica", 14),
        )
        self.loading_label.pack(pady=10)
        self.loading_label.pack_forget()  # Hide initially

        # Instructions
        self.instructions_label = ctk.CTkLabel(
            self,
            text="Translate the sentence from your native language to your target language.\n"
            "Press Enter to check your answer or click the Check Translation button.",
            font=("Helvetica", 12),
        )
        self.instructions_label.pack(pady=10)

        # Progress label
        self.progress_label = ctk.CTkLabel(self, text="", font=("Helvetica", 12))
        self.progress_label.pack(pady=5)

    def load_practice_sentences(self):
        """Load sentences for translation practice"""
        self.test_words = self.vocab_controller.get_translation_practice_sentences(5)

        if len(self.test_words) > 0:
            self.show_question(0)
        else:
            self.show_no_words_message()

    def show_question(self, idx: int):
        """Display the question at the specified index"""
        if idx < len(self.test_words):
            word = self.test_words.iloc[idx]

            # Clear previous state
            self.feedback_label.configure(text="")
            self.translation_entry.delete("0.0", "end")
            self.answer_checked = False
            self.is_checking = False

            # Configure buttons correctly
            self.next_button.pack_forget()
            self.check_button.configure(state="normal")
            self.dont_know_button.configure(state="normal")

            # Show native sentence
            self.native_sentence_label.configure(text=word["example_translation"])

            # Update progress
            self.progress_label.configure(
                text=f"Sentence {idx + 1} of {len(self.test_words)}"
            )

            # Focus the entry field
            self.translation_entry.focus_set()

    def handle_enter(self):
        """Handle enter key press - either check answer or advance to next question"""
        if not self.answer_checked and not self.is_checking:
            self.check_answer()
        elif self.answer_checked:
            self.next_question()

    def check_answer(self):
        """Check the user's translation using LLM"""
        if self.current_word_idx < len(self.test_words) and not self.is_checking:
            # Get current word data
            word = self.test_words.iloc[self.current_word_idx]

            # Get user's translation
            user_translation = self.translation_entry.get("0.0", "end").strip()

            if not user_translation:
                self.feedback_label.configure(
                    text="Please enter a translation before checking.",
                    text_color="orange",
                )
                return

            # Show loading indicator
            self.loading_label.pack(pady=10)
            self.check_button.configure(state="disabled")
            self.dont_know_button.configure(state="disabled")
            self.is_checking = True

            # Run check in a separate thread to keep UI responsive
            settings = self.vocab_controller.user_controller.get_settings()
            native_lang = settings["native_language"]
            target_lang = settings["target_language"]

            # Get the original sentence from the vocabulary
            original_sentence = word["example_translation"]  # In native language

            def check_translation_thread():
                try:
                    # Call the LLM to check the translation
                    result = self.vocab_controller.check_sentence_translation(
                        original_sentence=original_sentence,
                        translation=user_translation,
                        native_lang=native_lang,
                        target_lang=target_lang,
                    )

                    # Update the UI with the result (must be done in the main thread)
                    self.after(0, lambda: self.display_check_result(result, word))
                except Exception as e:
                    # Handle any errors
                    self.after(0, lambda: self.display_error(str(e)))

            # Start the check in a separate thread
            threading.Thread(target=check_translation_thread, daemon=True).start()

    def display_check_result(self, result, word):
        """Display the check result from the LLM"""
        # Hide loading indicator
        self.loading_label.pack_forget()

        # Update word statistics
        self.vocab_controller.update_word_stats(word["word"], result["is_correct"])

        if result["is_correct"]:
            self.feedback_label.configure(
                text=f"✓ Correct!\n\n{result['comment']}", text_color="green"
            )
            self.correct_answers += 1
        else:
            self.feedback_label.configure(
                text=f"✗ Needs improvement\n\n{result['comment']}\n\nReference translation: {word['example']}",
                text_color="orange",
            )

        # Disable buttons and show next
        self.check_button.configure(state="disabled")
        self.dont_know_button.configure(state="disabled")
        self.next_button.pack(pady=10)

        # Mark answer as checked
        self.answer_checked = True
        self.is_checking = False

    def display_error(self, error_message):
        """Display error message if translation check fails"""
        # Hide loading indicator
        self.loading_label.pack_forget()

        # Show error message
        self.feedback_label.configure(
            text=f"Error checking translation: {error_message}\n\nPlease try again.",
            text_color="red",
        )

        # Show both buttons again
        self.check_button.configure(state="normal")
        self.dont_know_button.configure(state="normal")

        # Reset checking state
        self.is_checking = False

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
            text="No words available for translation practice yet!\n\n"
            "Please review some words in the flashcard view first.",
            font=("Helvetica", 20),
        )
        message_label.pack(pady=20)

        # Clear instructions and progress
        self.instructions_label.configure(text="")
        self.progress_label.configure(text="")

        # Add button to go back to menu
        back_btn = ctk.CTkButton(
            self.question_frame, text="Return to Menu", command=self.on_complete
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
            text=f"Sentence Translation Practice Complete!\n\nScore: {self.correct_answers}/{total_questions}"
            f" ({score_percentage:.1f}%)\n\nGreat job practicing translations!",
            font=("Helvetica", 20),
        )
        completion_label.pack(pady=20)

        # Clear instructions
        self.instructions_label.configure(text="")

        # Update progress label
        self.progress_label.configure(text="")

        # Move to menu view
        self.after(2000, self.on_complete)

    def show_correct_translation(self):
        """Show the correct translation without calling LLM"""
        if self.current_word_idx < len(self.test_words) and not self.is_checking:
            # Get current word data
            word = self.test_words.iloc[self.current_word_idx]

            # Update word's last_practiced timestamp without affecting statistics
            # Note: We don't count this as a wrong answer, we just update the last_practiced timestamp
            self.vocab_controller.vocabulary.loc[
                self.vocab_controller.vocabulary["word"] == word["word"],
                "last_practiced",
            ] = datetime.now()
            self.vocab_controller.save_vocabulary()

            # Show correct translation
            self.feedback_label.configure(
                text=f"Reference translation: {word['example']}\n\n"
                f"It's okay if you don't know yet. Keep practicing!",
                text_color="#9C27B0",  # Use purple color for "I don't know" feedback
            )

            # Hide check button and show next button
            self.check_button.configure(state="disabled")
            self.dont_know_button.configure(state="disabled")
            self.next_button.pack(pady=10)

            # Mark answer as checked
            self.answer_checked = True
