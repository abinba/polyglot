# SentenceTestView

## Overview
The `SentenceTestView` provides an interactive test to practice vocabulary in context through sentence completion exercises. It presents sentences with missing words and multiple-choice options, helping users understand how words are used in real sentences.

## Class Definition
```python
class SentenceTestView(ctk.CTkFrame):
    def __init__(self, parent, vocab_controller: VocabularyController, on_complete: Callable):
        # Initialize the view with required dependencies
```

## Dependencies
- `customtkinter`: For creating the UI components
- `VocabularyController`: For retrieving test data and tracking progress
- `Callable`: For navigation callback
- `random`: For shuffling answer options

## UI Components
- **Title**: "Sentence Practice" at the top of the view
- **Question Frame**: Container for the current question
  - **Sentence Label**: Displays a sentence with a blank to fill
  - **Options Frame**: Contains the multiple choice options
  - **Translation Label**: Shows the sentence translation after answering
  - **Feedback Label**: Provides feedback on the answer
- **Instructions Label**: Provides guidance on how to interact with the test
- **Progress Label**: Shows progress through the test

## Key Methods

### setup_ui()
Sets up all UI components, including the question frame, options, and feedback areas.

### load_test_words()
Loads words for the test session.
- Retrieves test words from the vocabulary controller
- Displays the first question or a message if no words are available

### show_question(idx: int)
Displays the sentence question at the specified index.
- Updates the sentence with blank
- Shuffles and displays the multiple-choice options
- Tracks the correct answer index
- Resets the UI state for a new question
- Updates the progress indicator

### handle_space()
Handles space key press based on the current state.
- If answer not checked, checks the answer
- If answer already checked, moves to next question

### select_option(option_idx: int)
Handles selection of a multiple-choice option.
- Records the selected option
- Triggers answer checking

### check_answer()
Evaluates the selected answer and provides feedback.
- Determines if the selected option is correct
- Updates word statistics through the vocabulary controller
- Updates UI with feedback (correct/incorrect)
- Shows the sentence translation
- Disables option buttons to prevent changing answer
- Highlights the correct and selected options with color coding

### next_question()
Moves to the next question or completes the test.
- Increments the question index
- Shows the next question or completion screen if done

### show_no_words_message()
Displays a message when no words are available for testing.
- Informs the user that they need to review words first
- Provides a button to go to flashcards

### show_completion()
Shows completion message and final score.
- Calculates score as percentage of correct answers
- Displays the score and congratulatory message
- Automatically navigates to the next view after a delay

## User Interaction
- **Option Selection**: User clicks on an option to select their answer
- **Space Key**: Proceeds through the test (check answer or next question)

## Visual Feedback
- **Correct Answer**: Green highlight on the selected option
- **Incorrect Answer**: Red highlight on the selected option, green on the correct option
- **Feedback Text**: Confirms if answer was correct and shows the correct answer if wrong
- **Translation**: Shows the full sentence translation after answering

## Error Handling
- Validates that test words have required format (options, correct answer)
- Shows appropriate message if no words are available for testing

## Navigation
- After completing the test, automatically proceeds to the next view
- If no words are available, provides option to go to flashcards
