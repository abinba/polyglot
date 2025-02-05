import json
from pathlib import Path
from typing import Dict, List

class UserController:
    def __init__(self):
        self.data_dir = Path.home() / ".polyglot"
        self.user_file = self.data_dir / "user_settings.json"
        self.load_settings()
    
    def load_settings(self):
        """Load user settings from JSON file"""
        if self.user_file.exists():
            with open(self.user_file, 'r') as f:
                self.settings = json.load(f)
        else:
            self.settings = {
                'native_language': None,
                'target_language': None,
                'level': None,
                'topics': [],
                'include_phrases': True,
                'words_per_day': 5,
                'flashcard_delay': 5,
                'test_word_count': 10
            }
    
    def save_settings(self):
        """Save user settings to JSON file"""
        with open(self.user_file, 'w') as f:
            json.dump(self.settings, f)
    
    def user_exists(self) -> bool:
        """Check if user settings exist"""
        return self.user_file.exists()
    
    def create_user(self, native_lang: str, target_lang: str,
                   level: str, topics: List[str],
                   include_phrases: bool = True):
        """Create new user settings"""
        self.settings.update({
            'native_language': native_lang,
            'target_language': target_lang,
            'level': level,
            'topics': topics,
            'include_phrases': include_phrases
        })
        self.save_settings()
    
    def update_settings(self, settings: Dict):
        """Update user settings"""
        self.settings.update(settings)
        self.save_settings()
    
    def get_settings(self) -> Dict:
        """Get current user settings"""
        return self.settings.copy()
    
    @property
    def words_per_day(self) -> int:
        """Get number of words per day setting"""
        return self.settings.get('words_per_day', 5)
    
    @property
    def flashcard_delay(self) -> int:
        """Get flashcard delay in seconds"""
        return self.settings.get('flashcard_delay', 5)
    
    @property
    def test_word_count(self) -> int:
        """Get number of words for testing"""
        return self.settings.get('test_word_count', 10)
