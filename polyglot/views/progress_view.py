import customtkinter as ctk
from typing import Callable
import pandas as pd
from polyglot.controllers.vocabulary_controller import VocabularyController
from polyglot.views.base_view import BaseView
from datetime import datetime


class ProgressView(BaseView):
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

        self.setup_ui()
        self.load_progress()

        # Add back to menu button if callback provided
        if self.on_menu_click:
            self.add_back_to_menu_button(self.on_menu_click)

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

    def load_progress(self):
        """Load and display progress data"""
        # Get progress data
        progress_data = self.vocab_controller.get_progress()

        # Ensure required columns exist
        required_columns = ["times_practiced", "correct_answers", "last_practiced"]
        for col in required_columns:
            if col not in progress_data.columns:
                if col == "times_practiced" or col == "correct_answers":
                    progress_data[col] = 0
                elif col == "last_practiced":
                    progress_data[col] = datetime.now()

        # Calculate statistics
        total_words = len(progress_data)

        # Get learning thresholds from settings
        min_practice = self.vocab_controller.user_controller.min_practice_count
        min_success = (
            self.vocab_controller.user_controller.min_success_rate / 100
        )  # Convert to decimal

        # Words learnt (practiced >= min_practice times with >= min_success rate)
        # Avoid division by zero by adding a condition
        words_learnt = len(
            progress_data[
                (progress_data["times_practiced"] >= min_practice)
                & (progress_data["times_practiced"] > 0)  # Avoid division by zero
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

        ctk.CTkLabel(headers_frame, text="Status", font=("Helvetica", 14, "bold")).pack(
            side="right", padx=10
        )

        # Add separator
        separator = ctk.CTkFrame(self.vocab_frame, height=2, fg_color="gray")
        separator.pack(fill="x", pady=5)

        # Section headers for different status categories
        current_section = -1
        section_names = ["Not Started", "Needs Practice", "In Progress", "Learnt"]
        section_colors = [
            "#333333",
            "#882222",
            "#996600",
            "#227722",
        ]  # Dark, Red, Orange, Green

        # Display words
        for _, word in progress_data.iterrows():
            # Add section header if we're entering a new section
            status = int(word["learning_status"])
            if status != current_section:
                current_section = status

                # Add section divider
                if status > 0:  # Don't add divider before the first section
                    divider = ctk.CTkFrame(self.vocab_frame, height=1, fg_color="gray")
                    divider.pack(fill="x", pady=10)

                # Add section header
                section_frame = ctk.CTkFrame(self.vocab_frame)
                section_frame.pack(fill="x", pady=5)
                section_label = ctk.CTkLabel(
                    section_frame,
                    text=f"--- {section_names[status]} ---",
                    font=("Helvetica", 16, "bold"),
                )
                section_label.pack(pady=5)

            # Word frame
            word_frame = ctk.CTkFrame(self.vocab_frame)
            word_frame.pack(fill="x", pady=2)

            # Set appropriate background color based on status
            if status >= 0 and status < len(section_colors):
                word_frame.configure(fg_color=section_colors[status])

            # Word label
            word_label = ctk.CTkLabel(
                word_frame,
                text=f"{word['word']} ({word['translation']})",
                font=("Helvetica", 14),
            )
            word_label.pack(side="left", padx=10)

            # Create progress text
            times_practiced = word["times_practiced"]
            if times_practiced > 0:
                success_rate = word["success_rate"]  # Already as percentage
                progress_text = f"{success_rate:.1f}% ({times_practiced} attempts)"
            else:
                progress_text = "Not practiced yet"

            progress_label = ctk.CTkLabel(
                word_frame,
                text=progress_text,
                font=("Helvetica", 14),
            )
            progress_label.pack(side="right", padx=10)
