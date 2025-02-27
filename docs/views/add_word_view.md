# AddWordView

## Overview
The `AddWordView` provides a user interface for manually adding new words to the vocabulary. It allows users to enter a word and automatically generates the translation, example sentences, and other details using the language learning model.

## Class Definition
```python
class AddWordView(ctk.CTkFrame):
    def __init__(self, parent, vocab_controller: VocabularyController, on_complete: Callable):
        # Initialize the view with required dependencies
```

## Dependencies
- `customtkinter`: For creating the UI components
- `VocabularyController`: For vocabulary management operations
- `Callable`: For navigation callback

## UI Components
- **Title**: "Add New Word" at the top of the view
- **Word Input Field**: Text entry for the user to type the word they want to add
- **Translation Field** (auto-filled): Displays the generated translation
- **Example Field** (auto-filled): Displays a usage example in the target language
- **Example Translation Field** (auto-filled): Displays the translation of the example
- **Level Field** (auto-filled): Displays the difficulty level of the word
- **Generate Button**: Triggers the generation of word details
- **Add Button**: Adds the generated word to the vocabulary
- **Back Button**: Returns to the menu

## Key Methods

### setup_ui()
Sets up all UI components, including labels, entry fields, and buttons.

### generate_word_details()
Triggers the generation of word details using the language learning model.
- Validates the input word
- Disables the generate button to prevent multiple clicks
- Shows a progress indicator
- Schedules the actual generation to avoid UI freezing

### _do_generate_word_details()
Performs the actual word generation operation.
- Uses the vocabulary controller to generate word details
- Fills in the form fields with the generated data
- Enables the add button once generation is complete

### add_word()
Adds the generated word to the vocabulary.
- Disables the add button to prevent multiple clicks
- Shows a progress indicator
- Schedules the actual add operation to avoid UI freezing

### _do_add_word()
Performs the actual add operation.
- Adds the word to the vocabulary through the controller
- Clears the form fields
- Shows a success message
- Re-enables the generate button for the next word

## Usage Flow
1. User enters a word in the input field
2. User clicks "Generate Details" button
3. System generates and displays word details (translation, example, etc.)
4. User reviews the details
5. User clicks "Add Word" button
6. Word is added to vocabulary
7. Form is cleared for next entry

## Error Handling
- Shows error messages when generation or addition fails
- Prevents submission without entering a word
- Shows loading indicators during API operations

## Navigation
- "Back to Menu" button returns to the main menu
