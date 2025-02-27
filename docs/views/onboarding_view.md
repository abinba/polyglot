# OnboardingView

## Overview
The `OnboardingView` guides new users through the initial setup process, collecting necessary preferences to personalize the learning experience. This multi-step wizard gathers information about language preferences, proficiency level, topics of interest, and other learning settings.

## Class Definition
```python
class OnboardingView(ctk.CTkFrame):
    def __init__(self, parent, user_controller: UserController, vocab_controller: VocabularyController, on_complete: Callable):
        # Initialize the view with required dependencies
```

## Dependencies
- `customtkinter`: For creating the UI components
- `UserController`: For storing user preferences
- `VocabularyController`: For generating initial vocabulary
- `Callable`: For navigation callback after onboarding completion

## UI Components
- **Title**: "Welcome to Polyglot!" at the top of the view
- **Content Frame**: Dynamic area that changes based on the current step
- **Navigation Buttons**: Previous and Next/Finish buttons for moving between steps

## Onboarding Steps
The view presents a series of steps to collect user preferences:

1. **Native Language Selection**
   - Choose the user's native language from a list of options

2. **Target Language Selection**
   - Choose the language the user wants to learn

3. **Proficiency Level Selection**
   - Select current proficiency level (A1-C2)

4. **Topic Selection**
   - Choose topics of interest (multiple selection)

5. **Phrases Inclusion**
   - Option to include common phrases in vocabulary

## Key Methods

### setup_ui()
Sets up the basic UI structure with a content area and navigation buttons.

### show_step(step: int)
Displays the specified onboarding step.
- Clears the previous content
- Shows the appropriate step UI
- Updates navigation button states

### show_language_selection(lang_type: str)
Displays the language selection screen for either native or target language.
- Shows a list of available languages as buttons
- Highlights the currently selected language

### show_level_selection()
Displays the proficiency level selection screen.
- Shows available levels (A1, A2, B1, B2, C1, C2)
- Highlights the currently selected level

### show_topic_selection()
Displays the topic selection screen with multiple-choice options.
- Shows available topics as checkboxes
- Reflects the current selection state

### show_phrases_selection()
Displays the option to include common phrases in vocabulary.
- Shows a checkbox for enabling/disabling phrases

### select_language(lang_type: str, language: str)
Handles language selection for either native or target language.
- Updates the user data with the selected language
- Refreshes the current step to show the selection

### select_level(level: str)
Handles proficiency level selection.
- Updates the user data with the selected level
- Refreshes the current step to show the selection

### toggle_topic(topic: str)
Handles topic selection/deselection.
- Adds or removes the topic from the user's selected topics
- No UI refresh needed as checkboxes maintain their own state

### toggle_phrases(include: bool)
Handles phrases inclusion toggle.
- Updates the user data with the phrases preference

### prev_step()
Navigates to the previous step in the onboarding process.

### next_step()
Navigates to the next step or finishes onboarding if on the last step.

### finish_onboarding()
Completes the onboarding process with collected preferences.
- Saves user settings through the user controller
- Generates initial vocabulary based on preferences
- Navigates to the main application flow

## Usage Flow
1. User proceeds through each step of the onboarding process
2. User's preferences are collected at each step
3. After completing all steps, preferences are saved
4. Initial vocabulary is generated based on preferences
5. User is directed to the main application

## Navigation Controls
- **Previous Button**: Available after the first step, returns to previous step
- **Next Button**: Advances to the next step
- **Finish Button**: Replaces Next on the final step, completes onboarding
