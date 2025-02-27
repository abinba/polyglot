# MenuView

## Overview
The `MenuView` serves as the main navigation hub of the application, providing access to all major features and displaying basic status information. It organizes functionality into logical categories and provides an intuitive interface for users to navigate the application.

## Class Definition
```python
class MenuView(ctk.CTkFrame):
    def __init__(self, parent, vocab_controller: VocabularyController, user_controller: UserController, view_callbacks: Dict[str, Callable]):
        # Initialize the view with required dependencies
```

## Dependencies
- `customtkinter`: For creating the UI components
- `VocabularyController`: For vocabulary statistics
- `UserController`: For user settings
- `Dict[str, Callable]`: For navigation callbacks to different views

## UI Components
- **Welcome Section**: Displays the app title and vocabulary statistics
- **Practice Section**: Contains buttons for daily vocabulary review and exercises
  - **Words of the Day**: Access to daily vocabulary flashcards
  - **Exercise Session**: Access to practice exercises
- **Tests Section**: Contains buttons for different types of tests
  - **Word Translation**: Test for word translation knowledge
  - **Sentence Filling**: Test for using words in context
- **Tools Section**: Contains utility features
  - **Progress**: Access to progress tracking
  - **Add Word**: Tool for adding custom vocabulary
  - **Settings**: Application configuration

## Key Methods

### setup_ui()
Sets up all UI components, organized into sections for different categories of functionality.

### _create_menu_button(parent, text, description, command)
Helper method for creating consistent menu buttons with descriptions.
- Creates a button with the specified text and command
- Adds a description label for additional information
- Returns the created button for reference

### update_word_count()
Updates the word count display in the welcome section.
- Retrieves vocabulary statistics from the controller
- Calculates total words and learned words
- Updates the display with current statistics

## Usage Flow
1. User views the main menu with all available options
2. User selects a feature by clicking on the corresponding button
3. System navigates to the selected view using the appropriate callback

## Button Descriptions
Each button includes a helpful description to clarify its purpose:
- **Words of the Day**: "Review today's vocabulary"
- **Exercise Session**: "Complete practice session"
- **Word Translation**: "Test word translations"
- **Sentence Filling**: "Practice with sentences"
- **Progress**: "Track your learning"
- **Add Word**: "Add custom vocabulary"
- **Settings**: "Configure app settings"

## Statistics Display
The welcome section displays:
- Total number of words in the vocabulary
- Number of words considered "learned" (practiced ≥7 times with ≥75% success rate)

## Design Pattern
The MenuView uses the Command pattern through callback functions to navigate between views without tight coupling between components.
