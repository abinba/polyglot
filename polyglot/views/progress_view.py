import customtkinter as ctk
from typing import Callable
import pandas as pd
from polyglot.controllers.vocabulary_controller import VocabularyController


class ProgressView(ctk.CTkFrame):
    def __init__(
        self, parent, vocab_controller: VocabularyController, on_complete: Callable
    ):
        super().__init__(parent)
        self.vocab_controller = vocab_controller
        self.on_complete = on_complete

        self.setup_ui()
        self.load_progress()

    def setup_ui(self):
        """Set up the main UI components"""
        # Title
        self.title = ctk.CTkLabel(
            self, text="Your Progress", font=("Helvetica", 24, "bold")
        )
        self.title.pack(pady=20)

        # Progress frame
        self.progress_frame = ctk.CTkFrame(self)
        self.progress_frame.pack(pady=20, padx=40, fill="both", expand=True)

        # Statistics frame
        self.stats_frame = ctk.CTkFrame(self.progress_frame)
        self.stats_frame.pack(pady=10, padx=20, fill="x")

        # Words learned label
        self.words_learned_label = ctk.CTkLabel(
            self.stats_frame, text="", font=("Helvetica", 16)
        )
        self.words_learned_label.pack(pady=5)

        # Average success rate label
        self.success_rate_label = ctk.CTkLabel(
            self.stats_frame, text="", font=("Helvetica", 16)
        )
        self.success_rate_label.pack(pady=5)

        # Scrollable frame for vocabulary list
        self.vocab_frame = ctk.CTkScrollableFrame(self.progress_frame, height=400)
        self.vocab_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Navigation frame
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.pack(pady=20, fill="x")

        # Continue button
        self.continue_btn = ctk.CTkButton(
            self.nav_frame, text="Continue Learning", command=self.on_complete
        )
        self.continue_btn.pack(side="right", padx=20)

    def load_progress(self):
        """Load and display progress data"""
        # Get progress data
        progress_data = self.vocab_controller.get_progress()

        # Calculate statistics
        total_words = len(progress_data)
        words_practiced = len(progress_data[progress_data["times_practiced"] > 0])
        avg_success_rate = (
            progress_data["success_rate"].mean() * 100 if not progress_data.empty else 0
        )

        # Update statistics labels
        self.words_learned_label.configure(
            text=f"Words Learned: {words_practiced}/{total_words}"
        )
        self.success_rate_label.configure(
            text=f"Average Success Rate: {avg_success_rate:.1f}%"
        )

        # Display vocabulary list
        self.display_vocabulary(progress_data)

    def display_vocabulary(self, progress_data: pd.DataFrame):
        """Display vocabulary list with progress information"""
        # Clear previous content
        for widget in self.vocab_frame.winfo_children():
            widget.destroy()

        # Create headers
        headers_frame = ctk.CTkFrame(self.vocab_frame)
        headers_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(headers_frame, text="Word", font=("Helvetica", 14, "bold")).pack(
            side="left", padx=10
        )

        ctk.CTkLabel(
            headers_frame, text="Success Rate", font=("Helvetica", 14, "bold")
        ).pack(side="right", padx=10)

        # Add separator
        separator = ctk.CTkFrame(self.vocab_frame, height=2, fg_color="gray")
        separator.pack(fill="x", pady=5)

        # Display words
        for _, word in progress_data.iterrows():
            word_frame = ctk.CTkFrame(self.vocab_frame)
            word_frame.pack(fill="x", pady=2)

            # Word label
            word_label = ctk.CTkLabel(
                word_frame,
                text=f"{word['word']} ({word['translation']})",
                font=("Helvetica", 14),
            )
            word_label.pack(side="left", padx=10)

            # Progress indicators
            times_practiced = word["times_practiced"]
            success_rate = word["success_rate"] * 100 if times_practiced > 0 else 0

            progress_label = ctk.CTkLabel(
                word_frame,
                text=f"{success_rate:.1f}% ({times_practiced} attempts)",
                font=("Helvetica", 14),
            )
            progress_label.pack(side="right", padx=10)

            # Color coding based on success rate
            if times_practiced > 0:
                if success_rate >= 80:
                    word_frame.configure(fg_color="green")
                elif success_rate >= 50:
                    word_frame.configure(fg_color="orange")
                else:
                    word_frame.configure(fg_color="red")
