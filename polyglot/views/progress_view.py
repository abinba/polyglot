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

        # Info text
        min_practice = self.vocab_controller.user_controller.min_practice_count
        min_success = self.vocab_controller.user_controller.min_success_rate
        info_text = f"A word is considered 'learnt' when you have practiced it at least {min_practice} times "
        info_text += f"with a success rate of {min_success}% or higher."
        self.info_label = ctk.CTkLabel(
            self, text=info_text, font=("Helvetica", 10), wraplength=600
        )
        self.info_label.pack(pady=5)

        # Progress frame
        self.progress_frame = ctk.CTkFrame(self)
        self.progress_frame.pack(pady=20, padx=40, fill="both", expand=True)

        # Statistics frame
        self.stats_frame = ctk.CTkFrame(self.progress_frame)
        self.stats_frame.pack(pady=10, padx=20, fill="x")

        # Total words label
        self.total_words_label = ctk.CTkLabel(
            self.stats_frame, text="", font=("Helvetica", 16)
        )
        self.total_words_label.pack(pady=5)

        # Words learnt label
        self.words_learnt_label = ctk.CTkLabel(
            self.stats_frame, text="", font=("Helvetica", 16)
        )
        self.words_learnt_label.pack(pady=5)

        # Words in progress label
        self.words_in_progress_label = ctk.CTkLabel(
            self.stats_frame, text="", font=("Helvetica", 16)
        )
        self.words_in_progress_label.pack(pady=5)

        # Average success rate label
        self.success_rate_label = ctk.CTkLabel(
            self.stats_frame, text="", font=("Helvetica", 16)
        )
        self.success_rate_label.pack(pady=5)

        # Scrollable frame for vocabulary list
        self.vocab_frame = ctk.CTkScrollableFrame(
            self.progress_frame, height=350
        )  # Reduced height
        self.vocab_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Add a spacer frame to push content up
        spacer = ctk.CTkFrame(self, height=20)
        spacer.pack(fill="x")

        # Navigation frame at the bottom
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.pack(side="bottom", pady=20, padx=20, fill="x")

        # Continue button
        self.continue_btn = ctk.CTkButton(
            self.nav_frame,
            text="Continue Learning",
            command=self.on_complete,
            width=200,  # Make button wider
        )
        self.continue_btn.pack(side="right", padx=20)

    def load_progress(self):
        """Load and display progress data"""
        # Get progress data
        progress_data = self.vocab_controller.get_progress()

        # Calculate statistics
        total_words = len(progress_data)

        # Get learning thresholds from settings
        min_practice = self.vocab_controller.user_controller.min_practice_count
        min_success = (
            self.vocab_controller.user_controller.min_success_rate / 100
        )  # Convert to decimal

        # Words learnt (practiced >= min_practice times with >= min_success rate)
        words_learnt = len(
            progress_data[
                (progress_data["times_practiced"] >= min_practice)
                & (
                    progress_data["correct_answers"] / progress_data["times_practiced"]
                    >= min_success
                )
            ]
        )

        # Words in progress (practiced but not yet learnt)
        words_in_progress = len(
            progress_data[
                (progress_data["times_practiced"] > 0)
                & ~(
                    (progress_data["times_practiced"] >= min_practice)
                    & (
                        progress_data["correct_answers"]
                        / progress_data["times_practiced"]
                        >= min_success
                    )
                )
            ]
        )

        # Average success rate for practiced words
        practiced_words = progress_data[progress_data["times_practiced"] > 0]
        avg_success_rate = (
            (
                practiced_words["correct_answers"] / practiced_words["times_practiced"]
            ).mean()
            * 100
            if not practiced_words.empty
            else 0
        )

        # Update statistics labels
        self.total_words_label.configure(text=f"Total Words: {total_words}")
        self.words_learnt_label.configure(text=f"Words Learnt: {words_learnt}")
        self.words_in_progress_label.configure(
            text=f"Words in Progress: {words_in_progress}"
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

            # Determine status and color
            # Get learning thresholds from settings
            min_practice = self.vocab_controller.user_controller.min_practice_count
            min_success = (
                self.vocab_controller.user_controller.min_success_rate / 100
            )  # Convert to decimal

            if (
                times_practiced >= min_practice
                and (word["correct_answers"] / times_practiced) >= min_success
            ):
                word_frame.configure(fg_color="green")  # Learnt
                status = "Learnt"
            elif times_practiced > 0:
                success_rate = (word["correct_answers"] / times_practiced) * 100
                if success_rate >= 60:
                    word_frame.configure(fg_color="orange")  # Good progress
                    status = "In Progress"
                else:
                    word_frame.configure(fg_color="red")  # Needs practice
                    status = "Needs Practice"
            else:
                status = "Not Started"

            # Create progress text
            if times_practiced > 0:
                success_rate = (word["correct_answers"] / times_practiced) * 100
                progress_text = (
                    f"{success_rate:.1f}% ({times_practiced} attempts) - {status}"
                )
            else:
                progress_text = status

            progress_label = ctk.CTkLabel(
                word_frame,
                text=progress_text,
                font=("Helvetica", 14),
            )
            progress_label.pack(side="right", padx=10)
