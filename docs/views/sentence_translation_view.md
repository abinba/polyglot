# SentenceTranslationView

## Overview
The `SentenceTranslationView` provides an advanced language learning exercise where users translate complete sentences from their native language to their target language. This view leverages an LLM-powered analysis to provide detailed feedback on the quality and correctness of translations, helping users develop more nuanced language understanding.

## Class Definition
```python
class SentenceTranslationView(ctk.CTkFrame):
    def __init__(self, parent, vocab_controller: VocabularyController, on_complete: Callable):
        # Initialize the view with required dependencies
```

## Dependencies
- `customtkinter`: For creating the UI components
- `VocabularyController`: For retrieving practice sentences and checking translations
- `threading`: For non-blocking LLM calls
- `Callable`: For navigation callback

## UI Components
- **Title**: "Sentence Translation Practice" at the top of the view
- **Question Frame**: Container for the translation exercise
  - **Native Sentence Label**: Displays the sentence to translate (in native language)
  - **Instruction Label**: Provides guidance on what to do
  - **Translation Entry**: Text field for entering the translation
  - **Check Button**: Button to evaluate the translation
  - **I Don't Know Button**: Button to skip the question and see the correct translation
  - **Feedback Label**: Provides detailed feedback on the translation
  - **Next Button**: Advances to the next sentence (appears after checking)
  - **Loading Label**: Indicates when translation is being checked
- **Instructions Label**: Explains how to use the view
- **Progress Label**: Shows progress through the practice session

## Key Methods

### setup_ui()
Sets up all UI components, including the question frame, translation entry, and feedback areas.

### load_practice_sentences()
Loads sentences for translation practice.
- Retrieves practice sentences from the vocabulary controller
- Shows the first sentence or completion message if no sentences are available

### show_question(idx: int)
Displays the question at the specified index.
- Updates the sentence to translate
- Clears previous answer and feedback
- Updates the progress indicator
- Resets the check button and I don't know button states

### handle_enter()
Handles enter key press based on the current state.
- If answer not checked, checks the answer
- If answer already checked, moves to next question

### check_answer()
Evaluates the user's translation using the LLM.
- Shows loading indicator
- Disables the check and I don't know buttons
- Creates a background thread to call the translation checking service

### show_correct_translation()
Shows the correct translation without calling the LLM.
- Updates word statistics (marks as incorrect)
- Displays the reference translation
- Shows the next button
- Provides encouraging message to the user

### display_check_result(result, word)
Displays the result of the translation check.
- Updates word statistics through the vocabulary controller
- Shows feedback with detailed comments from the LLM
- Displays the next button

### next_question()
Moves to the next question or completes the practice session.
- Increments the question index
- Shows the next question or completion screen if done

### show_completion()
Shows completion message and final score.
- Calculates score as percentage of correct translations
- Displays the score and motivational message
- Automatically navigates to the menu after a delay

## Translation Analysis
The LLM-based translation analysis provides:
- Boolean correctness assessment (is_correct)
- Detailed feedback with explanations
- Grammar rule citations when relevant
- Suggestions for improvement
- Positive reinforcement for correct translations

## User Interaction
- **Text Entry**: User types their translation in the text field
- **Check Button**: User clicks to evaluate their translation
- **I Don't Know Button**: User clicks to skip and see the correct translation
- **Enter Key**: Can be used to check answer or advance to next question
- **Next Button**: Advances to the next sentence after receiving feedback

## Visual Feedback
- **Feedback Text**: Provides detailed analysis of the translation
- **Color Coding**: Green for correct translations, orange for translations needing improvement
- **Loading Indicator**: Shows when translation is being checked

## Learning Integration
- Sentences are selected from the vocabulary database
- Performance is tracked and used to update learning statistics
- Prioritizes sentences using words with lower success rates

## Navigation
- After completing all sentences, automatically returns to the menu view

## Error Handling
- Shows appropriate error messages if LLM service fails
- Allows retrying the translation check if an error occurs
