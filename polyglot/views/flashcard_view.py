import customtkinter as ctk
from typing import Callable
import pandas as pd
from polyglot.controllers.vocabulary_controller import VocabularyController
from polyglot.views.base_view import BaseView


class FlashcardView(BaseView):
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
        self.words = None
        self.card_flipped = False

        self.setup_ui()
        self.load_words()

        # Add back to menu button if callback provided
        if self.on_menu_click:
            self.add_back_to_menu_button(self.on_menu_click)

        # Bind keyboard events to the parent window
        self.master.bind("<space>", lambda e: self.flip_card())
        self.master.bind("<Right>", lambda e: self.next_word())

    def setup_ui(self):
        """Set up the main UI components"""
        # Title
        self.title = ctk.CTkLabel(
            self, text="Learn New Words", font=("Helvetica", 24, "bold")
        )
        self.title.pack(pady=20)

        # Flashcard frame
        self.card_frame = ctk.CTkFrame(self, width=400, height=300)
        self.card_frame.pack(pady=20, padx=40, fill="both", expand=True)
        self.card_frame.pack_propagate(False)

        # Word label
        self.word_label = ctk.CTkLabel(self.card_frame, text="", font=("Helvetica", 20))
        self.word_label.pack(pady=20)

        # Translation label
        self.translation_label = ctk.CTkLabel(
            self.card_frame, text="", font=("Helvetica", 18)
        )
        self.translation_label.pack(pady=10)

        # Example label
        self.example_label = ctk.CTkLabel(
            self.card_frame, text="", font=("Helvetica", 16), wraplength=350
        )
        self.example_label.pack(pady=10)

        # Example translation label
        self.example_translation_label = ctk.CTkLabel(
            self.card_frame, text="", font=("Helvetica", 16), wraplength=350
        )
        self.example_translation_label.pack(pady=10)

        # Navigation frame
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.pack(pady=20, fill="x")

        # Flip button
        self.flip_btn = ctk.CTkButton(
            self.nav_frame, text="Flip Card (Space)", command=self.flip_card
        )
        self.flip_btn.pack(side="left", padx=20)

        # Next button
        self.next_btn = ctk.CTkButton(
            self.nav_frame, text="Next (→)", command=self.next_word
        )
        self.next_btn.pack(side="right", padx=20)

        # Progress label
        self.progress_label = ctk.CTkLabel(self, text="", font=("Helvetica", 14))
        self.progress_label.pack(pady=10)

    def load_words(self):
        """Load words for today's learning session"""
        self.words = self.vocab_controller.get_flashcard_words(
            count=self.vocab_controller.user_controller.words_per_day
        )
        if not self.words.empty:
            self.show_word(0)
        else:
            self.show_completion()

    def show_word(self, idx: int):
        """Display the word at the specified index"""
        if idx < len(self.words):
            word = self.words.iloc[idx]
            self.word_label.configure(text=word["word"])
            self.translation_label.configure(text="")
            self.example_label.configure(text="")
            self.example_translation_label.configure(text="")
            self.card_flipped = False

            # Mark word as viewed
            self.vocab_controller.mark_word_as_viewed(word["word"])

            # Update progress
            self.progress_label.configure(text=f"Word {idx + 1} of {len(self.words)}")

    def flip_card(self):
        """Flip the flashcard to show/hide translation and example"""
        if not self.card_flipped and self.current_word_idx < len(self.words):
            word = self.words.iloc[self.current_word_idx]
            self.translation_label.configure(text=word["translation"])
            self.example_label.configure(text=word["example"])
            self.example_translation_label.configure(text=word["example_translation"])
            self.card_flipped = True

    def next_word(self):
        """Move to the next word or complete the session"""
        if self.current_word_idx < len(self.words):
            # Update word statistics
            word = self.words.iloc[self.current_word_idx]
            self.vocab_controller.update_word_stats(word["word"], True)

            self.current_word_idx += 1
            if self.current_word_idx < len(self.words):
                self.show_word(self.current_word_idx)
            else:
                self.show_completion()

    def show_completion(self):
        """Show completion message and move to test"""
        # Clear card frame
        for widget in self.card_frame.winfo_children():
            widget.destroy()

        # Show completion message
        completion_label = ctk.CTkLabel(
            self.card_frame,
            text="You've learned all new words!\nLet's test your knowledge!",
            font=("Helvetica", 20),
        )
        completion_label.pack(pady=20)

        # Update navigation
        self.flip_btn.configure(state="disabled")
        self.next_btn.configure(text="Start Test", command=self.on_complete)
