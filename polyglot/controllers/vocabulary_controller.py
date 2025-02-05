import pandas as pd
import json
from pathlib import Path
import os
from typing import List, Dict, Optional
from pydantic import BaseModel

from polyglot.services.llm_provider import OpenAIProvider, LlmChatCompletionResponse
from polyglot.controllers.user_controller import UserController

class WordResponse(BaseModel):
    word: str
    translation: str
    example: str
    topic: Optional[str] = None
    level: Optional[str] = None


class Words(BaseModel):
    words: List[WordResponse]


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
                api_key=self.api_key,
                model="gpt-4o-2024-08-06"
            )
    
    def load_vocabulary(self):
        """Load vocabulary from CSV file"""
        if self.vocab_file.exists():
            self.vocabulary = pd.read_csv(self.vocab_file)
        else:
            self.vocabulary = pd.DataFrame(columns=[
                'word', 'translation', 'example', 'times_practiced',
                'correct_answers', 'topic', 'level'
            ])
    
    def save_vocabulary(self):
        """Save vocabulary to CSV file"""
        self.vocabulary.to_csv(self.vocab_file, index=False)
    
    def generate_words(self, native_lang: str, target_lang: str, level: str,
                      topics: List[str], include_phrases: bool,
                      exclude_words: List[str] = None) -> List[Dict]:
        """Generate new words using OpenAI API"""
        if not self.api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        # Get existing words to exclude
        existing_words = self.vocabulary['word'].tolist()
        if exclude_words:
            existing_words.extend(exclude_words)
        
        system_prompt = {
            "role": "system",
            "content": """You are a language learning assistant. Generate vocabulary items in the requested format.
            Each item should include:
            - word: the word in the target language
            - translation: the word in the native language
            - example: a natural example sentence
            - topic: the topic category (optional)
            - level: the CEFR level (optional)
            Focus on practical, commonly used vocabulary appropriate for the specified level.
            Do not repeat words that are in the exclude list."""
        }
        
        user_prompt = {
            "role": "user",
            "content": f"""Generate 10 words/phrases for language learning:
            - From {native_lang} to {target_lang}
            - Level: {level}
            - Topics: {', '.join(topics)}
            - Include phrases: {include_phrases}
            """
        }
        
        if existing_words:
            user_prompt["content"] += f"\nExclude these words: {', '.join(existing_words)}"
        
        response: LlmChatCompletionResponse = self.llm_provider.get_chat_completion(
            messages=[system_prompt, user_prompt],
            response_format=Words,
            temperature=0.7,
            max_tokens=5000
        )
        
        # Process the response and ensure all fields are present
        words = Words.model_validate(response.dict_response)
        return words.dict()['words']
    
    def add_words(self, words: List[Dict]):
        """Add new words to vocabulary"""
        for word in words:
            new_row = {
                'word': word['word'],
                'translation': word['translation'],
                'example': word['example'],
                'times_practiced': 0,
                'correct_answers': 0,
                'topic': word.get('topic', ''),
                'level': word.get('level', '')
            }
            self.vocabulary = pd.concat([
                self.vocabulary,
                pd.DataFrame([new_row])
            ], ignore_index=True)
        self.save_vocabulary()
    
    def get_unpracticed_words(self) -> pd.DataFrame:
        """Get words that haven't been practiced yet"""
        return self.vocabulary[self.vocabulary['times_practiced'] == 0]
    
    def get_daily_words(self, count: int) -> pd.DataFrame:
        """Get words for daily practice, prioritizing unpracticed words"""
        # First get unpracticed words
        unpracticed = self.get_unpracticed_words()
        if len(unpracticed) >= count:
            return unpracticed.head(count)
        
        # If we need more words, get the least practiced ones
        needed = count - len(unpracticed)
        practiced = self.vocabulary[self.vocabulary['times_practiced'] > 0]
        least_practiced = practiced.nsmallest(needed, 'times_practiced')
        
        # Combine unpracticed and least practiced words
        return pd.concat([unpracticed, least_practiced])
    
    def needs_new_words(self, min_unpracticed: int = 5) -> bool:
        """Check if we need to generate new words based on unpracticed count"""
        unpracticed_count = len(self.get_unpracticed_words())
        return unpracticed_count < min_unpracticed
    
    def get_test_words(self, count: int) -> pd.DataFrame:
        """Get words for testing"""
        return self.vocabulary.sample(n=min(count, len(self.vocabulary)))
    
    def update_word_stats(self, word: str, correct: bool):
        """Update statistics for a word after practice"""
        idx = self.vocabulary.index[self.vocabulary['word'] == word].tolist()[0]
        self.vocabulary.at[idx, 'times_practiced'] += 1
        if correct:
            self.vocabulary.at[idx, 'correct_answers'] += 1
        self.save_vocabulary()
    
    def get_progress(self) -> pd.DataFrame:
        """Get vocabulary progress sorted by success rate"""
        self.vocabulary['success_rate'] = (
            self.vocabulary['correct_answers'] / 
            self.vocabulary['times_practiced'].where(
                self.vocabulary['times_practiced'] > 0, 1
            )
        )
        return self.vocabulary.sort_values('success_rate', ascending=False)
