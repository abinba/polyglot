import pandas as pd
import json
from pathlib import Path
import os
from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import datetime

from polyglot.services.llm_provider import OpenAIProvider, LlmChatCompletionResponse
from polyglot.controllers.user_controller import UserController


class WordResponse(BaseModel):
    word: str
    translation: str
    example: str
    example_translation: str
    topic: Optional[str] = None
    level: Optional[str] = None
    sentence_to_fill: str
    sentence_to_fill_translation: str
    options: List[str]
    correct_answer: str


class Words(BaseModel):
    words: List[WordResponse]


class TranslationCheckResponse(BaseModel):
    is_correct: bool
    comment: str


class VocabularyController:
    def __init__(self, user_controller: UserController):
        self.data_dir = Path.home() / ".polyglot"
        self.vocab_file = self.data_dir / "vocabulary.csv"
        self.user_controller = user_controller
        self.load_vocabulary()

        # Initialize OpenAI provider
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.llm_provider = OpenAIProvider(
                api_key=self.api_key, model="gpt-4o-2024-08-06"
            )

    def load_vocabulary(self):
        """Load vocabulary from CSV file"""
        if self.vocab_file.exists():
            try:
                # First load with minimal type specifications to avoid NA errors
                self.vocabulary = pd.read_csv(self.vocab_file)

                # Convert options in a vectorized way if present
                if "options" in self.vocabulary.columns:
                    # Check if options column is string type before applying eval
                    self.vocabulary["options"] = self.vocabulary["options"].apply(
                        lambda x: eval(x) if isinstance(x, str) else x
                    )

                # Initialize or convert last_practiced
                if "last_practiced" not in self.vocabulary.columns:
                    self.vocabulary["last_practiced"] = datetime.now()
                else:
                    # Convert string dates to datetime objects
                    try:
                        self.vocabulary["last_practiced"] = pd.to_datetime(
                            self.vocabulary["last_practiced"], errors="coerce"
                        )
                        # Fill NaN values with current datetime (fixed to avoid FutureWarning)
                        mask = self.vocabulary["last_practiced"].isna()
                        self.vocabulary.loc[mask, "last_practiced"] = datetime.now()
                    except Exception:
                        # If conversion fails, set to current datetime
                        self.vocabulary["last_practiced"] = datetime.now()

                # Ensure required columns exist with default values
                required_columns = {
                    "correct_answers": 0,
                    "times_practiced": 0,
                    "viewed": False,
                }

                for col, default in required_columns.items():
                    if col not in self.vocabulary.columns:
                        self.vocabulary[col] = default
                    elif self.vocabulary[col].isnull().any():
                        # Use .loc instead of fillna with inplace=True
                        mask = self.vocabulary[col].isnull()
                        self.vocabulary.loc[mask, col] = default

                # Convert integer columns after filling NAs
                integer_columns = ["times_practiced", "correct_answers"]
                for col in integer_columns:
                    if col in self.vocabulary.columns:
                        self.vocabulary[col] = self.vocabulary[col].astype(int)

                # Convert boolean columns
                if "viewed" in self.vocabulary.columns:
                    self.vocabulary["viewed"] = self.vocabulary["viewed"].astype(bool)

            except Exception as e:
                print(f"Error loading vocabulary: {e}")
                # Create a new empty vocabulary as fallback
                self.vocabulary = pd.DataFrame(
                    columns=[
                        "word",
                        "translation",
                        "example",
                        "example_translation",
                        "times_practiced",
                        "correct_answers",
                        "topic",
                        "level",
                        "sentence_to_fill",
                        "sentence_to_fill_translation",
                        "options",
                        "correct_answer",
                        "viewed",
                        "last_practiced",
                    ]
                )
        else:
            # Create empty DataFrame with all required columns
            self.vocabulary = pd.DataFrame(
                columns=[
                    "word",
                    "translation",
                    "example",
                    "example_translation",
                    "times_practiced",
                    "correct_answers",
                    "topic",
                    "level",
                    "sentence_to_fill",
                    "sentence_to_fill_translation",
                    "options",
                    "correct_answer",
                    "viewed",
                    "last_practiced",
                ]
            )

    def save_vocabulary(self):
        """Save vocabulary to CSV file"""
        # Create a copy for saving to avoid modifying the original
        vocab_to_save = self.vocabulary.copy()

        # Process options columns efficiently
        if "options" in vocab_to_save.columns:
            vocab_to_save["options"] = vocab_to_save["options"].apply(str)

        # Convert datetime objects to ISO format strings for saving
        if "last_practiced" in vocab_to_save.columns:
            # Handle different data types that might exist in the column
            vocab_to_save["last_practiced"] = vocab_to_save["last_practiced"].apply(
                lambda x: x.isoformat() if hasattr(x, "isoformat") else str(x)
            )

        # Use efficient CSV writing
        vocab_to_save.to_csv(self.vocab_file, index=False)

    def generate_words(
        self,
        native_lang: str,
        target_lang: str,
        level: str,
        topics: List[str],
        include_phrases: bool,
        exclude_words: List[str] = None,
        custom_word: str = None,
    ) -> List[Dict]:
        """Generate new words using OpenAI API"""
        if not self.api_key:
            raise ValueError("OpenAI API key not found in environment variables")

        # If custom_word is provided, generate details for just that word
        if custom_word:
            return [
                self.generate_word_details(custom_word, native_lang, target_lang, level)
            ]

        # Get existing words to exclude
        existing_words = self.vocabulary["word"].tolist()
        if exclude_words:
            existing_words.extend(exclude_words)

        system_prompt = {
            "role": "system",
            "content": """You are a language learning assistant. Generate vocabulary items in the requested format.
            Each item should include:
            - word: the word in the target language
            - translation: the word in the native language
            - example: a natural example sentence
            - example_translation: translation of the example sentence
            - topic: the topic category (optional)
            - level: the CEFR level (optional)
            - sentence_to_fill: a different example sentence with a blank where the word should go
            - sentence_to_fill_translation: translation of the sentence_to_fill with the word included
            - options: list of 4 words (including the correct answer) that could fit grammatically
            - correct_answer: the correct word (same as 'word')
            
            Focus on practical, commonly used vocabulary appropriate for the specified level.
            The sentence_to_fill should be different from the example sentence.
            The options should be grammatically valid but only one should make sense in context.
            Do not repeat words that are in the exclude list.""",
        }

        user_prompt = {
            "role": "user",
            "content": f"""Generate 15 words/phrases for language learning:
            - From {native_lang} to {target_lang}
            - Level: {level}
            - Topics: {", ".join(topics)}
            - Include phrases: {include_phrases}
            """,
        }

        if existing_words:
            user_prompt["content"] += (
                f"\nExclude these words: {', '.join(existing_words)}"
            )

        response: LlmChatCompletionResponse = self.llm_provider.get_chat_completion(
            messages=[system_prompt, user_prompt],
            response_format=Words,
            temperature=0.7,
            max_tokens=5000,
        )

        # Process the response and ensure all fields are present
        words = Words.model_validate(response.dict_response)
        return words.dict()["words"]

    def generate_word_details(
        self, word: str, native_lang: str, target_lang: str, level: str
    ) -> Dict:
        """Generate details for a single word using OpenAI API"""
        if not self.api_key:
            raise ValueError("OpenAI API key not found in environment variables")

        system_prompt = {
            "role": "system",
            "content": """You are a language learning assistant. Generate details for the given word in the requested format.
            The response should include:
            - word: the word in the target language (use the provided word)
            - translation: the word in the native language
            - example: a natural example sentence using the word
            - example_translation: translation of the example sentence
            - topic: a relevant topic category
            - level: the CEFR level (use the provided level)
            - sentence_to_fill: a different example sentence with a blank where the word should go
            - sentence_to_fill_translation: translation of the sentence_to_fill with the word included
            - options: list of 4 words (including the correct answer) that could fit grammatically
            - correct_answer: the correct word (same as the provided word)
            
            The sentence_to_fill should be different from the example sentence.
            The options should be grammatically valid but only one (the correct answer) should make sense in context.""",
        }

        user_prompt = {
            "role": "user",
            "content": f"""Generate details for this word/phrase:
            - Word: {word}
            - From {native_lang} to {target_lang}
            - Level: {level}
            """,
        }

        response: LlmChatCompletionResponse = self.llm_provider.get_chat_completion(
            messages=[system_prompt, user_prompt],
            response_format=WordResponse,
            temperature=0.7,
            max_tokens=1000,
        )

        # Process the response and ensure all fields are present
        word_details = WordResponse.model_validate(response.dict_response)
        return word_details.dict()

    def add_words(self, words: List[Dict]):
        """Add new words to vocabulary"""
        for word in words:
            # Skip if word already exists
            if word["word"] in self.vocabulary["word"].values:
                continue

            # Ensure options is a list of exactly 4 items
            options = word["options"]
            if not isinstance(options, list) or len(options) != 4:
                raise ValueError(f"Word {word['word']} must have exactly 4 options")

            new_row = {
                "word": word["word"],
                "translation": word["translation"],
                "example": word["example"],
                "example_translation": word["example_translation"],
                "times_practiced": 0,
                "correct_answers": 0,
                "topic": word.get("topic", ""),
                "level": word.get("level", ""),
                "sentence_to_fill": word["sentence_to_fill"],
                "sentence_to_fill_translation": word["sentence_to_fill_translation"],
                "options": options,
                "correct_answer": word["correct_answer"],
                "viewed": False,
                "last_practiced": None,
            }
            self.vocabulary = pd.concat(
                [self.vocabulary, pd.DataFrame([new_row])], ignore_index=True
            )
        self.save_vocabulary()

    def get_unpracticed_words(self) -> pd.DataFrame:
        """Get words that haven't been practiced yet"""
        return self.vocabulary[self.vocabulary["times_practiced"] == 0]

    def get_daily_words(self, count: int) -> pd.DataFrame:
        """Get words for daily practice, prioritizing unpracticed words and including some old words"""
        # First get unpracticed words (up to count-2 to leave room for review words)
        unpracticed = self.get_unpracticed_words()
        unpracticed_count = min(len(unpracticed), count - 2)
        selected_unpracticed = (
            unpracticed.sample(n=unpracticed_count)
            if unpracticed_count > 0
            else pd.DataFrame()
        )

        # Get words that were learned a long time ago (practiced >= 7 times)
        old_words = self.vocabulary[
            (
                self.vocabulary["times_practiced"]
                >= self.user_controller.min_practice_count
            )
            & (
                self.vocabulary["correct_answers"] / self.vocabulary["times_practiced"]
                >= self.user_controller.min_success_rate / 100
            )
        ]

        # If we have old words, select 1-2 randomly
        old_word_count = min(len(old_words), 2)
        selected_old = (
            old_words.sample(n=old_word_count) if old_word_count > 0 else pd.DataFrame()
        )

        # Calculate how many more words we need
        needed = count - len(selected_unpracticed) - len(selected_old)

        # Get the least practiced words for the remaining slots
        practiced = self.vocabulary[
            ~self.vocabulary.index.isin(selected_unpracticed.index)
            & ~self.vocabulary.index.isin(selected_old.index)
            & (self.vocabulary["times_practiced"] > 0)
        ]
        least_practiced = (
            practiced.nsmallest(needed, "times_practiced")
            if needed > 0
            else pd.DataFrame()
        )

        # Combine all selected words and shuffle
        result = pd.concat([selected_unpracticed, selected_old, least_practiced])
        return result.sample(frac=1)  # Shuffle the final selection

    def needs_new_words(self, min_unpracticed: int = 5) -> bool:
        """Check if we need to generate new words based on unpracticed count"""
        unpracticed_count = len(self.get_unpracticed_words())
        return unpracticed_count < min_unpracticed

    def get_test_words(self, count: int) -> pd.DataFrame:
        """Get words for testing, prioritizing rarely practiced words and words practiced long ago"""
        # Get words that have been viewed
        viewed_words = self.vocabulary[self.vocabulary["viewed"] == True].copy()

        if viewed_words.empty:
            return pd.DataFrame()  # Return empty DataFrame if no words have been viewed

        # Calculate success rate for words that have been practiced
        viewed_words["success_rate"] = 0.0  # Default for unpracticed words
        mask = viewed_words["times_practiced"] > 0
        if mask.any():
            viewed_words.loc[mask, "success_rate"] = (
                viewed_words.loc[mask, "correct_answers"]
                / viewed_words.loc[mask, "times_practiced"]
            )

        # Split the selection into two parts:
        # 1. Words rarely practiced or with lower success rates
        # 2. Words practiced long ago

        # Sort by times_practiced (ascending) and success_rate (ascending)
        rare_practiced_words = viewed_words.sort_values(
            by=["times_practiced", "success_rate"], ascending=[True, True]
        )

        # Sort by last_practiced (ascending - older first)
        old_practiced_words = viewed_words.sort_values(
            by=["last_practiced"], ascending=[True]
        )

        # Select half from rarely practiced and half from long ago practiced
        half_count = count // 2
        remainder = count % 2  # In case count is odd

        rare_selected = rare_practiced_words.head(half_count + remainder)
        old_selected = old_practiced_words[
            ~old_practiced_words.index.isin(rare_selected.index)
        ].head(half_count)

        # Combine and shuffle
        result = pd.concat([rare_selected, old_selected])
        return result.sample(min(len(result), count))

    def get_flashcard_words(self, count: int) -> pd.DataFrame:
        """Get words for flashcards, only returning unviewed words"""
        # Only get unviewed words
        unviewed_words = self.vocabulary[self.vocabulary["viewed"] == False].copy()

        if unviewed_words.empty:
            return pd.DataFrame()  # Return empty DataFrame if no unviewed words

        # Return a random sample of unviewed words
        return unviewed_words.sample(min(len(unviewed_words), count))

    def mark_word_as_viewed(self, word: str):
        """Mark a word as viewed"""
        idx = self.vocabulary.index[self.vocabulary["word"] == word].tolist()[0]
        self.vocabulary.at[idx, "viewed"] = True
        self.vocabulary.at[idx, "last_practiced"] = datetime.now()
        self.save_vocabulary()

    def update_word_stats(self, word: str, correct: bool):
        """Update statistics for a word after practice"""
        idx = self.vocabulary.index[self.vocabulary["word"] == word].tolist()[0]
        self.vocabulary.at[idx, "times_practiced"] += 1
        if correct:
            self.vocabulary.at[idx, "correct_answers"] += 1
        self.vocabulary.at[idx, "last_practiced"] = datetime.now()
        self.save_vocabulary()

    def get_progress(self) -> pd.DataFrame:
        """
        Get vocabulary progress data categorized and sorted by learning status

        Returns a DataFrame with the following columns:
        - word: The word or phrase
        - translation: The word's translation
        - success_rate: The percentage of correct answers
        - times_practiced: The number of times the word has been practiced
        - learning_status: A numerical value representing the learning status:
            0 = Not started (never practiced)
            1 = Needs practice (practiced with low success rate)
            2 = In progress (practiced with good progress)
            3 = Learnt (meets minimum practice and success criteria)
        """
        # Get all words
        all_words = self.vocabulary.copy()

        if len(all_words) == 0:
            return pd.DataFrame(
                columns=[
                    "word",
                    "translation",
                    "success_rate",
                    "times_practiced",
                    "learning_status",
                ]
            )

        # Calculate success rate for words that have been practiced
        all_words["success_rate"] = 0.0  # Default for unpracticed words
        mask = all_words["times_practiced"] > 0
        if mask.any():
            all_words.loc[mask, "success_rate"] = (
                all_words.loc[mask, "correct_answers"]
                / all_words.loc[mask, "times_practiced"]
            )

        # Get learning thresholds from settings
        min_practice = self.user_controller.min_practice_count
        min_success = self.user_controller.min_success_rate / 100  # Convert to decimal

        # Determine learning status for sorting
        all_words["learning_status"] = 0  # Default: Not started

        # Words that have been practiced but with low success rate
        mask_needs_practice = (all_words["times_practiced"] > 0) & (
            all_words["success_rate"] < 0.6
        )
        all_words.loc[mask_needs_practice, "learning_status"] = 1  # Needs practice

        # Words with good progress
        mask_in_progress = (
            (all_words["times_practiced"] > 0)
            & (all_words["success_rate"] >= 0.6)
            & (
                (all_words["times_practiced"] < min_practice)
                | (all_words["success_rate"] < min_success)
            )
        )
        all_words.loc[mask_in_progress, "learning_status"] = 2  # In progress

        # Words that are fully learnt
        mask_learnt = (all_words["times_practiced"] >= min_practice) & (
            all_words["success_rate"] >= min_success
        )
        all_words.loc[mask_learnt, "learning_status"] = 3  # Learnt

        # Convert success rate to percentage
        all_words["success_rate"] = all_words["success_rate"] * 100

        # Sort by learning status (ascending) and success rate (descending)
        sorted_words = all_words.sort_values(
            by=["learning_status", "success_rate"], ascending=[True, False]
        )

        # Return the relevant columns
        return sorted_words[
            [
                "word",
                "translation",
                "success_rate",
                "times_practiced",
                "learning_status",
            ]
        ]

    def check_sentence_translation(
        self,
        original_sentence: str,
        translation: str,
        native_lang: str,
        target_lang: str,
    ) -> Dict:
        """Check a sentence translation using OpenAI API"""
        if not self.api_key:
            raise ValueError("OpenAI API key not found in environment variables")

        system_prompt = {
            "role": "system",
            "content": """You are a language learning assistant. Evaluate the user's translation of a sentence.
            
            You will receive:
            1. Original sentence in one language
            2. User's translation in another language
            
            Evaluate the translation and provide:
            - is_correct: boolean indicating if the translation is correct (true or false)
            - comment: helpful feedback on the translation
            
            For translations that are not correct, provide specific feedback about what's wrong
            and how to improve it. Mention relevant grammar rules or vocabulary issues.
            
            Even for correct translations, provide a short encouraging comment or a note about
            a nuance of the translation.
            """,
        }

        user_prompt = {
            "role": "user",
            "content": f"""Evaluate this translation:
            
            Original ({native_lang}): {original_sentence}
            Translation ({target_lang}): {translation}
            """,
        }

        response: LlmChatCompletionResponse = self.llm_provider.get_chat_completion(
            messages=[system_prompt, user_prompt],
            response_format=TranslationCheckResponse,
            temperature=0.3,
            max_tokens=500,
        )

        # Process the response
        check_result = TranslationCheckResponse.model_validate(response.dict_response)
        return check_result.dict()

    def get_translation_practice_sentences(self, count: int) -> pd.DataFrame:
        """Get sentences for translation practice from vocabulary pool, balanced between practice frequency and time since last practice"""
        if len(self.vocabulary) == 0:
            return pd.DataFrame()

        # Create a copy of the vocabulary to work with
        all_words = self.vocabulary.copy()

        # Split the selection into two parts:
        # 1. Words that haven't been practiced much (fewer attempts)
        # 2. Words that were practiced long ago

        # Calculate success rate for words that have been practiced
        all_words["success_rate"] = all_words.apply(
            lambda row: row["correct_answers"] / row["times_practiced"]
            if row["times_practiced"] > 0
            else 0,
            axis=1,
        )

        # Sort by times_practiced (ascending)
        low_practice_words = all_words.sort_values(
            by=["times_practiced"], ascending=[True]
        )

        # Sort by last_practiced (ascending - older first)
        old_practice_words = all_words.sort_values(
            by=["last_practiced"], ascending=[True]
        )

        # Select half from each category
        half_count = count // 2
        remainder = count % 2  # In case count is odd

        low_practice_selected = low_practice_words.head(half_count + remainder)
        old_practice_selected = old_practice_words[
            ~old_practice_words.index.isin(low_practice_selected.index)
        ].head(half_count)

        # Combine and shuffle
        result = pd.concat([low_practice_selected, old_practice_selected])
        return result.sample(min(len(result), count))

    def delete_word(self, word: str) -> bool:
        """Delete a word from the vocabulary

        Args:
            word: The word to delete

        Returns:
            bool: True if word was successfully deleted, False otherwise
        """
        try:
            # Find the word and remove it
            word_indices = self.vocabulary.index[
                self.vocabulary["word"] == word
            ].tolist()
            if not word_indices:
                print(f"Word '{word}' not found in vocabulary")
                return False

            # Drop all matching indices (should usually be just one)
            self.vocabulary = self.vocabulary.drop(word_indices)

            # Reset index after dropping rows
            self.vocabulary = self.vocabulary.reset_index(drop=True)

            # Save the updated vocabulary
            self.save_vocabulary()
            return True
        except Exception as e:
            print(f"Error deleting word: {e}")
            return False
