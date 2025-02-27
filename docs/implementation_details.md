# Polyglot Implementation Details

This document provides technical implementation details for the Polyglot language learning application, focusing on architecture, data flows, and algorithms.

## Architecture

Polyglot follows the Model-View-Controller (MVC) architectural pattern:

### Controllers

1. **Application Controller**: Main controller coordinating all application components
   - Manages view transitions
   - Initializes other controllers
   - Handles application lifecycle

2. **Vocabulary Controller**: Manages vocabulary operations
   - Vocabulary data access and persistence
   - Word generation using OpenAI API
   - Learning algorithms and statistics

3. **User Controller**: Manages user-related operations
   - User settings persistence
   - Preference management
   - Session tracking

### Views

The UI layer consists of multiple views, each implemented as a customtkinter Frame:
- See [Views Documentation](views/index.md) for details on each view

### Services

1. **OpenAI Service**: Interfaces with OpenAI API
   - Word generation
   - Sentence generation
   - Translation services

2. **Data Service**: Manages data persistence
   - File operations for vocabulary and settings
   - Data migration and upgrades
   - Backup and recovery

## Data Flow

### User Onboarding Flow
```
User Input → OnboardingView → UserController.create_user() → 
VocabularyController.generate_words() → VocabularyController.add_words() → MenuView
```

### Learning Flow
```
MenuView → FlashcardView → VocabularyController.get_daily_words() → 
User Review → VocabularyController.mark_word_as_viewed() → 
TestView → VocabularyController.get_test_words() → 
VocabularyController.update_word_stats() → ProgressView
```

### Settings Update Flow
```
MenuView → SettingsView → User Input → 
UserController.update_settings() → Settings Persistence
```

## Data Structures

### Vocabulary Data (CSV)
- `word`: Target language word or phrase
- `translation`: Native language translation
- `example`: Example sentence in target language
- `example_translation`: Example sentence translation
- `level`: Difficulty level (A1-C2)
- `last_practiced`: Timestamp of last practice
- `times_practiced`: Count of practice sessions
- `correct_answers`: Count of correct answers
- `topics`: List of associated topics

### User Settings (JSON)
- `native_language`: User's native language
- `target_language`: Language being learned
- `level`: User's proficiency level
- `topics`: Preferred topics
- `include_phrases`: Whether to include phrases
- `words_per_day`: Daily word count
- `flashcard_delay`: Flashcard timing
- `test_word_count`: Words per test session
- `min_practice_count`: Practices required to learn
- `min_success_rate`: Success rate required to learn

## Algorithms

### Word Selection Algorithm
1. Filter vocabulary by minimum review date
2. Prioritize words by:
   - Lower mastery level (times_practiced and success rate)
   - Higher relevance to user topics
   - Appropriate difficulty level
3. Select top N words for daily review

### Learning Criteria
A word is considered "learnt" when:
1. It has been practiced at least `min_practice_count` times
2. The success rate (correct_answers / times_practiced) is ≥ `min_success_rate`

### Test Generation
1. Select words for testing based on:
   - Recently viewed words
   - Words with lower mastery levels
   - Words not tested recently
2. For multiple choice options:
   - Select distractors with similar difficulty
   - Avoid obvious non-matches
   - Include at least one similar word when possible

## External APIs

### OpenAI API Integration
- Model: GPT-4
- API Endpoint: https://api.openai.com/v1/chat/completions
- Authentication: API key from environment variables
- Prompt structure: JSON templates for vocabulary generation

## File Locations

- User settings: `~/.polyglot/user_settings.json`
- Vocabulary: `~/.polyglot/vocabulary.csv`
- Logs: `~/.polyglot/logs/`

## Performance Considerations

1. **API Cost Optimization**:
   - Batch generation of words
   - Caching of API responses
   - Local generation of test variations

2. **Memory Usage**:
   - Lazy loading of vocabulary data
   - Pagination of large word lists
   - Resource cleanup on view transitions

## Next Steps

For common issues and edge cases, see [Gotchas](gotchas.md).
