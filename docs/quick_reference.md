# Polyglot Quick Reference

This document provides a quick reference for key parameters, configurations, and common operations in the Polyglot application.

## Configuration Parameters

### User Settings

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `words_per_day` | 5 | 1-50 | Number of new words presented daily |
| `flashcard_delay` | 5 | 1-30 | Auto-flip timing for flashcards (seconds) |
| `test_word_count` | 10 | 5-50 | Number of words in test sessions |
| `min_practice_count` | 7 | 1-20 | Practices required to consider a word learnt |
| `min_success_rate` | 75 | 1-100 | Success percentage required to consider a word learnt |

### Language Options

| Category | Available Options |
|----------|-------------------|
| Languages | English, Spanish, French, German, Italian, Portuguese, Russian, Chinese, Japanese, Korean |
| Levels | A1, A2, B1, B2, C1, C2 |
| Topics | Business, Travel, Technology, Culture, Food, Sports, Education, Entertainment, Science, Nature |

## File Locations

| File | Path | Description |
|------|------|-------------|
| User Settings | `~/.polyglot/user_settings.json` | User preferences and configuration |
| Vocabulary | `~/.polyglot/vocabulary.csv` | Word data and learning statistics |
| Logs | `~/.polyglot/logs/app.log` | Application logs |

## Data Schemas

### Vocabulary CSV Columns

| Column | Type | Description |
|--------|------|-------------|
| `word` | str | Target language word or phrase |
| `translation` | str | Native language translation |
| `example` | str | Example sentence in target language |
| `example_translation` | str | Example sentence translation |
| `level` | str | Difficulty level (A1-C2) |
| `topics` | list | Associated topics |
| `last_practiced` | datetime | When the word was last practiced |
| `times_practiced` | int | Number of practice sessions |
| `correct_answers` | int | Number of correct answers |
| `times_viewed` | int | Number of times viewed in flashcards |
| `last_viewed` | datetime | When the word was last viewed |

### User Settings JSON Structure

```json
{
  "native_language": "English",
  "target_language": "Spanish",
  "level": "B1",
  "topics": ["Travel", "Food", "Technology"],
  "include_phrases": true,
  "words_per_day": 5,
  "flashcard_delay": 5,
  "test_word_count": 10,
  "min_practice_count": 7,
  "min_success_rate": 75
}
```

## Key Methods and Functions

### Vocabulary Management

| Method | Purpose | Example |
|--------|---------|---------|
| `generate_words(...)` | Generate new vocabulary words | `vocab_controller.generate_words(native_lang="English", target_lang="Spanish", level="B1", topics=["Travel"])` |
| `add_words(words)` | Add words to vocabulary | `vocab_controller.add_words(generated_words)` |
| `get_daily_words(count)` | Get words for daily learning | `vocab_controller.get_daily_words(count=5)` |
| `get_test_words(count)` | Get words for testing | `vocab_controller.get_test_words(count=10)` |
| `mark_word_as_viewed(word)` | Mark word as viewed | `vocab_controller.mark_word_as_viewed("hola")` |
| `update_word_stats(word, is_correct)` | Update learning statistics | `vocab_controller.update_word_stats("hola", True)` |
| `check_sentence_translation(...)` | Check translation using LLM | `vocab_controller.check_sentence_translation(original_sentence="Hello", translation="Hola", native_lang="English", target_lang="Spanish")` |
| `get_translation_practice_sentences(count)` | Get sentences for translation practice | `vocab_controller.get_translation_practice_sentences(count=5)` |

### User Management

| Method | Purpose | Example |
|--------|---------|---------|
| `create_user(...)` | Create new user profile | `user_controller.create_user(native_lang="English", target_lang="Spanish")` |
| `get_settings()` | Get current user settings | `settings = user_controller.get_settings()` |
| `update_settings(settings)` | Update user settings | `user_controller.update_settings({"words_per_day": 10})` |

## OpenAI API

### API Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| `API_KEY` | From `.env` | OpenAI API key for authentication |
| `MODEL` | "gpt-4" | Language model to use |
| `TEMPERATURE` | 0.7 | Creativity level for generation |
| `MAX_TOKENS` | 1500 | Maximum response length |

### API Prompt Structure

```python
{
    "model": "gpt-4",
    "messages": [
        {"role": "system", "content": "You are a helpful language learning assistant..."},
        {"role": "user", "content": f"Generate {count} words in {target_lang} for a {level} level learner..."}
    ],
    "temperature": 0.7,
    "max_tokens": 1500
}
```

## Common Command Patterns

### Running the Application

```bash
# From the project root
python -m polyglot.app

# With debug logging
POLYGLOT_DEBUG=1 python -m polyglot.app
```

### Data Operations

```bash
# Backup vocabulary
cp ~/.polyglot/vocabulary.csv ~/.polyglot/backups/vocabulary_$(date +%Y%m%d).csv

# Reset user settings
rm ~/.polyglot/user_settings.json

# View vocabulary statistics
wc -l ~/.polyglot/vocabulary.csv
```

## Keyboard Shortcuts

| View | Key | Action |
|------|-----|--------|
| FlashcardView | Space | Flip card |
| FlashcardView | Right Arrow | Next word |
| TestView | Space/Enter | Check answer or next question |
| SentenceTestView | Space | Check answer or next question |

## Error Codes

| Error Code | Description | Solution |
|------------|-------------|----------|
| `API_001` | OpenAI API key missing | Set the API key in .env file |
| `API_002` | OpenAI API rate limit | Wait and retry with exponential backoff |
| `API_003` | OpenAI API error | Check connection and API status |
| `DATA_001` | Data file not found | Ensure directories exist and are writable |
| `DATA_002` | Data file corrupted | Restore from backup or reinitialize |
| `UI_001` | UI rendering error | Check Python and customtkinter versions |
