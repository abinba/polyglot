import customtkinter as ctk
from typing import Callable
from polyglot.controllers.vocabulary_controller import VocabularyController
from polyglot.views.base_view import BaseView


class AddWordView(BaseView):
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

        # Add back to menu button if callback provided
        if self.on_menu_click:
            self.add_back_to_menu_button(self.on_menu_click)

    def setup_ui(self):
        """Set up the main UI components"""
        # Title
        self.title = ctk.CTkLabel(
            self, text="Add New Word", font=("Helvetica", 24, "bold")
        )
        self.title.pack(pady=20)

        # Scroll frame for the form
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(pady=20, padx=40, fill="both", expand=True)

        # Form frame inside scroll frame
        self.form_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.form_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Word input
        self.word_label = ctk.CTkLabel(
            self.form_frame, text="Word:", font=("Helvetica", 16)
        )
        self.word_label.pack(pady=(10, 0), padx=20, anchor="w")

        self.word_entry = ctk.CTkEntry(
            self.form_frame, width=300, placeholder_text="Enter word or phrase"
        )
        self.word_entry.pack(pady=(0, 10), padx=20)

        # Translation (auto-filled)
        self.translation_label = ctk.CTkLabel(
            self.form_frame, text="Translation:", font=("Helvetica", 16)
        )
        self.translation_label.pack(pady=(10, 0), padx=20, anchor="w")

        self.translation_entry = ctk.CTkEntry(
            self.form_frame, width=300, state="disabled"
        )
        self.translation_entry.pack(pady=(0, 10), padx=20)

        # Example (auto-filled)
        self.example_label = ctk.CTkLabel(
            self.form_frame, text="Example:", font=("Helvetica", 16)
        )
        self.example_label.pack(pady=(10, 0), padx=20, anchor="w")

        self.example_entry = ctk.CTkTextbox(
            self.form_frame, width=300, height=60, state="disabled"
        )
        self.example_entry.pack(pady=(0, 10), padx=20)

        # Example translation (auto-filled)
        self.example_trans_label = ctk.CTkLabel(
            self.form_frame, text="Example Translation:", font=("Helvetica", 16)
        )
        self.example_trans_label.pack(pady=(10, 0), padx=20, anchor="w")

        self.example_trans_entry = ctk.CTkTextbox(
            self.form_frame, width=300, height=60, state="disabled"
        )
        self.example_trans_entry.pack(pady=(0, 10), padx=20)

        # Level (auto-filled)
        self.level_label = ctk.CTkLabel(
            self.form_frame, text="Level:", font=("Helvetica", 16)
        )
        self.level_label.pack(pady=(10, 0), padx=20, anchor="w")

        self.level_entry = ctk.CTkEntry(self.form_frame, width=300, state="disabled")
        self.level_entry.pack(pady=(0, 10), padx=20)

        # Status label
        self.status_label = ctk.CTkLabel(
            self.form_frame, text="", font=("Helvetica", 14), text_color="red"
        )
        self.status_label.pack(pady=10, padx=20)

        # Buttons frame at the bottom of main view
        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.pack(pady=20, padx=40, fill="x", side="bottom")

        # Generate button
        self.generate_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Generate Details",
            command=self.generate_word_details,
        )
        self.generate_btn.pack(side="left", padx=10, expand=True)

        # Add button
        self.add_btn = ctk.CTkButton(
            self.buttons_frame, text="Add Word", command=self.add_word, state="disabled"
        )
        self.add_btn.pack(side="left", padx=10, expand=True)

    def generate_word_details(self):
        """Generate word details using the LLM"""
        word = self.word_entry.get().strip()
        if not word:
            self.status_label.configure(text="Please enter a word first")
            return

        try:
            # Disable generate button and show progress
            self.generate_btn.configure(state="disabled")
            self.status_label.configure(
                text="Generating word details...", text_color="blue"
            )

            # Create progress bar
            self.progress_bar = ctk.CTkProgressBar(
                self.buttons_frame, mode="indeterminate", width=300
            )
            self.progress_bar.pack(pady=(0, 10), padx=20)
            self.progress_bar.start()

            # Schedule the generation to avoid freezing UI
            self.after(100, self._do_generate_word_details)

        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}", text_color="red")
            self.generate_btn.configure(state="normal")

    def _do_generate_word_details(self):
        """Actually perform the word generation"""
        try:
            word = self.word_entry.get().strip()

            # Generate a single word with all details
            words = self.vocab_controller.generate_words(
                native_lang=self.vocab_controller.user_controller.settings[
                    "native_language"
                ],
                target_lang=self.vocab_controller.user_controller.settings[
                    "target_language"
                ],
                level=self.vocab_controller.user_controller.settings["level"],
                topics=["custom"],
                include_phrases=False,
                exclude_words=[],
                custom_word=word,
            )

            if not words:
                self.status_label.configure(
                    text="Failed to generate word details", text_color="red"
                )
                return

            # Fill in the details
            generated = words[0]
            self.translation_entry.configure(state="normal")
            self.translation_entry.delete(0, "end")
            self.translation_entry.insert(0, generated["translation"])
            self.translation_entry.configure(state="disabled")

            self.example_entry.configure(state="normal")
            self.example_entry.delete("1.0", "end")
            self.example_entry.insert("1.0", generated["example"])
            self.example_entry.configure(state="disabled")

            self.example_trans_entry.configure(state="normal")
            self.example_trans_entry.delete("1.0", "end")
            self.example_trans_entry.insert("1.0", generated["example_translation"])
            self.example_trans_entry.configure(state="disabled")

            self.level_entry.configure(state="normal")
            self.level_entry.delete(0, "end")
            self.level_entry.insert(0, generated["level"])
            self.level_entry.configure(state="disabled")

            # Store the full generated word data
            self.generated_word = generated

            # Enable add button
            self.add_btn.configure(state="normal")
            self.status_label.configure(
                text="Word details generated successfully!", text_color="green"
            )

        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}", text_color="red")
        finally:
            # Re-enable generate button and remove progress bar
            self.generate_btn.configure(state="normal")
            if hasattr(self, "progress_bar"):
                self.progress_bar.stop()
                self.progress_bar.pack_forget()
                del self.progress_bar

    def add_word(self):
        """Add the word to vocabulary"""
        try:
            # Disable add button and show progress
            self.add_btn.configure(state="disabled")
            self.status_label.configure(
                text="Adding word to vocabulary...", text_color="blue"
            )

            # Create progress bar
            self.progress_bar = ctk.CTkProgressBar(
                self.buttons_frame, mode="indeterminate", width=300
            )
            self.progress_bar.pack(pady=(0, 10), padx=20)
            self.progress_bar.start()

            # Schedule the add operation to avoid freezing UI
            self.after(100, self._do_add_word)

        except Exception as e:
            self.status_label.configure(
                text=f"Error adding word: {str(e)}", text_color="red"
            )
            self.add_btn.configure(state="normal")

    def _do_add_word(self):
        """Actually perform the add operation"""
        try:
            self.vocab_controller.add_words([self.generated_word])

            # Clear form
            self.word_entry.delete(0, "end")
            self.translation_entry.configure(state="normal")
            self.translation_entry.delete(0, "end")
            self.translation_entry.configure(state="disabled")
            self.example_entry.configure(state="normal")
            self.example_entry.delete("1.0", "end")
            self.example_entry.configure(state="disabled")
            self.example_trans_entry.configure(state="normal")
            self.example_trans_entry.delete("1.0", "end")
            self.example_trans_entry.configure(state="disabled")
            self.level_entry.configure(state="normal")
            self.level_entry.delete(0, "end")
            self.level_entry.configure(state="disabled")

            # Reset the form for next word
            self.status_label.configure(
                text="Word added successfully! You can add another word.",
                text_color="green",
            )

            # Re-enable generate button for next word
            self.generate_btn.configure(state="normal")

        except Exception as e:
            self.status_label.configure(
                text=f"Error adding word: {str(e)}", text_color="red"
            )
            self.add_btn.configure(state="normal")
        finally:
            # Remove progress bar
            if hasattr(self, "progress_bar"):
                self.progress_bar.stop()
                self.progress_bar.pack_forget()
                del self.progress_bar
