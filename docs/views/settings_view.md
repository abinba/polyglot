# SettingsView

## Overview
The `SettingsView` allows users to customize their learning experience by adjusting various application settings. It provides a form-based interface to modify parameters such as daily word count, flashcard timing, and learning thresholds.

## Class Definition
```python
class SettingsView(ctk.CTkFrame):
    def __init__(self, parent, user_controller: UserController, on_complete: Callable):
        # Initialize the view with required dependencies
```

## Dependencies
- `customtkinter`: For creating the UI components
- `UserController`: For retrieving and updating user settings
- `Callable`: For navigation callback

## UI Components
- **Title**: "Settings" at the top of the view
- **Settings Frame**: Container for all settings controls
  - **Words per day**: Control for the number of new words per day
  - **Flashcard delay**: Control for flashcard display duration in seconds
  - **Words per test**: Control for the number of words in test sessions
  - **Minimum practices to learn**: Control for required practice count
  - **Minimum success rate**: Control for required success percentage
- **Navigation Buttons**:
  - **Save**: Saves changes and returns to previous view
  - **Cancel**: Discards changes and returns to previous view

## Key Methods

### setup_ui()
Sets up all UI components, including settings controls and navigation buttons.
- Creates frames for each setting
- Adds labels and input fields
- Sets up save and cancel buttons

### load_settings()
Loads current settings from the user controller.
- Retrieves settings values
- Sets the initial values in the input fields

### save_settings()
Validates, saves settings, and returns to the previous view.
- Parses and validates all input values
- Applies reasonable limits to each setting
- Updates settings through the user controller
- Navigates back to the previous view

## Settings Parameters

1. **Words per day**
   - Controls the number of new words shown in daily learning
   - Valid range: 1-50
   - Default: 5

2. **Flashcard delay**
   - Controls the auto-flip timing for flashcards (in seconds)
   - Valid range: 1-30
   - Default: 5

3. **Words per test**
   - Controls the number of words included in test sessions
   - Valid range: 5-50
   - Default: 10

4. **Minimum practices to learn**
   - Number of times a word must be practiced to be considered learned
   - Valid range: 1-20
   - Default: 7

5. **Minimum success rate**
   - Required success percentage to consider a word learned
   - Valid range: 1-100
   - Default: 75

## Input Validation
- All numeric inputs are validated to ensure they are within acceptable ranges
- Values outside the acceptable range are clamped to the nearest valid value
- Error messages are displayed for non-numeric input

## Error Handling
- Shows an error message when invalid input is detected
- Error message automatically disappears after a delay

## Navigation
- **Save Button**: Validates input, saves settings, and returns to previous view
- **Cancel Button**: Discards changes and returns to previous view
