# TestView

## Overview
The `TestView` provides an interactive test interface to evaluate the user's knowledge of vocabulary translations. It presents words for translation and offers multiple-choice options, tracking the user's performance and providing immediate feedback.

## Class Definition
```python
class TestView(ctk.CTkFrame):
    def __init__(self, parent, vocab_controller: VocabularyController, on_complete: Callable):
        # Initialize the view with required dependencies
```

## Dependencies
- `customtkinter`: For creating the UI components
- `VocabularyController`: For retrieving test words and tracking progress
- `Callable`: For navigation callback
- `random`: For shuffling answer options

## UI Components
- **Title**: "Translation Test" at the top of the view
- **Question Frame**: Container for the current question
  - **Word Label**: Displays the word to translate (in native language)
  - **Answer Entry**: Text field for typing answers
  - **Options Frame**: Contains multiple choice options
  - **Feedback Label**: Provides feedback on the answer
- **Instructions Label**: Provides guidance on how to interact with the test
- **Progress Label**: Shows progress through the test

## Key Methods

### setup_ui()
Sets up all UI components, including the question frame, answer field, and feedback areas.

### load_test_words()
Loads words for the test session.
- Retrieves test words from the vocabulary controller
- Displays the first question or completion message if no words are available

### show_question(idx: int)
Displays the question at the specified index.
- Updates the word to translate
- Clears previous answer and feedback
- Generates and displays multiple-choice options
- Updates the progress indicator

### generate_options(current_word)
Generates multiple-choice options for the current word.
- Selects random words from the vocabulary as distractors
- Adds the correct answer to the options
- Shuffles the options and creates option buttons

### select_option(option: str)
Handles selection of a multiple-choice option.
- Fills the answer entry with the selected option

### handle_space()
Handles space key press based on the current state.
- If answer not checked, checks the answer
- If answer already checked, moves to next question

### check_answer()
Evaluates the user's answer and provides feedback.
- Compares the user's answer with the correct translation
- Updates word statistics through the vocabulary controller
- Updates UI with feedback (correct/incorrect)
- Disables the answer entry to prevent changing answer

### next_question()
Moves to the next question or completes the test.
- Increments the question index
- Shows the next question or completion screen if done

### show_completion()
Shows completion message and final score.
- Calculates score as percentage of correct answers
- Displays the score and motivational message
- Automatically navigates to the sentence test after a delay

## User Interaction
- **Text Entry**: User can type their answer
- **Option Selection**: User can click on an option to select it
- **Space/Enter Key**: Proceeds through the test (check answer or next question)

## Visual Feedback
- **Feedback Text**: Confirms if answer was correct and shows the correct answer if wrong
- **Color Coding**: Green for correct answers, red for incorrect

## Learning Integration
- Tests are based on the user's vocabulary
- Performance is tracked and used to update learning statistics
- Successful answers increase the word's mastery level

## Navigation
- After completing the test, automatically proceeds to the sentence test

## Completion Flow
1. User completes all questions in the test
2. System displays the final score and performance
3. After a brief delay, system navigates to the sentence test for further practice
