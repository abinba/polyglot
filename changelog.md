# Polyglot Changelog

## [1.1.0] - 2025-02-27

### Added
- New **Sentence Translation Exercise**: Enables users to practice translating complete sentences from their native language to their target language
  - Sentences are drawn from the existing vocabulary pool, prioritizing words with lower success rates
  - Uses LLM-powered analysis to provide detailed feedback on translation quality and correctness
  - Provides specific grammar and vocabulary improvement suggestions
  - Includes an "I Don't Know" button to skip difficult sentences and see the correct translation
  - Integrates with the existing learning progression after the sentence test
  - Added "Back to Main Menu" button to all views
  - Added `last_practiced` field to vocabulary model
  - Added improved word selection for practice sessions based on practice history
  - Non-penalizing "I Don't Know" functionality - unsuccessful attempts don't count negatively
- New VocabularyController methods:
  - `check_sentence_translation()`: Evaluates translations using LLM
  - `get_translation_practice_sentences()`: Retrieves sentences for practice based on learning progress
- New documentation:
  - Added SentenceTranslationView documentation
  - Updated mental model to include the new exercise
  - Updated navigation flow documentation

### Changed
- Updated application flow: SentenceTestView now leads to SentenceTranslationView
- Modified MenuView to include direct access to sentence translation exercise
- Improved vocabulary progress analytics in the get_progress method
- Word selection for tests and sentence translation now considers both practice frequency and time since last practice
- Updated vocabulary controller to track when words were last practiced
- Refactored views to inherit from a common BaseView class
- Enhanced ProgressView to categorize words by learning status (Not Started, Needs Practice, In Progress, Learnt)
- Added color-coded indicators for learning status in ProgressView
- Updated the vocabulary progress calculation to track learning status
- Modified FlashcardView to only show unviewed/new words
- Improved ProgressView to categorize words by learning status:
  - Words are now grouped into "Not Started", "Needs Practice", "In Progress", and "Learnt" sections
  - Each section has a distinct color coding for better visual feedback
  - Words within each category are sorted by success rate
- Modified vocabulary controller to calculate learning status for words
- Enhanced vocabulary selection logic for tests to consider recency of practice
- Unsuccessful translation attempts no longer penalize the user's statistics

### Fixed
- Fixed an issue with missing vocabulary columns causing errors in ProgressView
- Fixed menu navigation through the application
- Fixed date handling for last_practiced field to properly convert between string and datetime formats
- Fixed test word selection to properly handle datetime sorting
