# FlashcardView

## Overview
The `FlashcardView` provides an interactive flashcard interface for learning new vocabulary. It displays words from the user's daily learning set one at a time, allowing users to review the translation and example usage.

## Class Definition
```python
class FlashcardView(ctk.CTkFrame):
    def __init__(self, parent, vocab_controller: VocabularyController, on_complete: Callable):
        # Initialize the view with required dependencies
```

## Dependencies
- `customtkinter`: For creating the UI components
- `VocabularyController`: For retrieving word data and tracking progress
- `Callable`: For navigation callback
- `pandas`: For data handling

## UI Components
- **Title**: "Learn New Words" at the top of the view
- **Card Frame**: Container for displaying the flashcard content
- **Word Label**: Displays the current word in the target language
- **Translation Label**: Displays the translation (hidden initially)
- **Example Label**: Displays an example sentence (hidden initially)
- **Example Translation Label**: Displays the translation of the example (hidden initially)
- **Flip Button**: Reveals the translation and example
- **Next Button**: Moves to the next word
- **Progress Label**: Shows progress through the learning session

## Key Methods

### setup_ui()
Sets up all UI components, including the card frame, labels, and navigation buttons.

### load_words()
Loads words for the daily learning session.
- Retrieves the daily words from the vocabulary controller
- Displays the first word or shows completion if no words are available

### show_word(idx: int)
Displays the word at the specified index.
- Updates the word label with the current word
- Hides the translation and example
- Marks the word as viewed in the vocabulary controller
- Updates the progress indicator

### flip_card()
Reveals the translation and example for the current word.
- Shows the translation, example sentence, and example translation
- Sets the card_flipped flag to prevent multiple flips

### next_word()
Moves to the next word or completes the session.
- Updates word statistics for the current word
- Increments the word index
- Shows the next word or completion message if finished

### show_completion()
Shows a completion message when all words have been reviewed.
- Clears the card frame
- Displays a completion message
- Updates navigation buttons for proceeding to the test

## Keyboard Shortcuts
- **Space**: Flips the card to reveal translation and example
- **Right Arrow**: Moves to the next word

## Usage Flow
1. System loads daily words for learning
2. User is shown each word one by one
3. User presses space to reveal translation and example
4. User presses right arrow or clicks "Next" to move to the next word
5. After reviewing all words, user is prompted to start a test

## Navigation
- On completion, automatically proceeds to the test view

## States
- **Word Display**: Shows only the target language word
- **Card Flipped**: Shows the word, translation, and example
- **Completion**: Shows a completion message and prompt for test
