# ProgressView

## Overview
The `ProgressView` displays the user's learning progress, showing statistics about vocabulary mastery and providing a detailed breakdown of each word's learning status. It helps users track their progress and identify areas that need more practice.

## Class Definition
```python
class ProgressView(ctk.CTkFrame):
    def __init__(self, parent, vocab_controller: VocabularyController, on_complete: Callable):
        # Initialize the view with required dependencies
```

## Dependencies
- `customtkinter`: For creating the UI components
- `VocabularyController`: For retrieving progress data
- `Callable`: For navigation callback
- `pandas`: For data handling

## UI Components
- **Title**: "Your Progress" at the top of the view
- **Info Label**: Explains the criteria for considering a word "learnt"
- **Statistics Frame**: Displays overall progress statistics
  - **Total Words**: Number of words in vocabulary
  - **Words Learnt**: Number of words meeting learning criteria
  - **Words in Progress**: Number of words partially learned
  - **Average Success Rate**: Average performance across all practiced words
- **Vocabulary List**: Scrollable list showing detailed progress for each word
  - **Word**: Word in target language with translation
  - **Progress**: Success rate, attempt count, and status
- **Continue Button**: Returns to the main learning flow

## Key Methods

### setup_ui()
Sets up all UI components, including the statistics section and vocabulary list area.

### load_progress()
Loads and displays progress data.
- Retrieves progress data from the vocabulary controller
- Calculates statistics based on the data
- Updates the statistics labels
- Calls display_vocabulary to show the detailed word list

### display_vocabulary(progress_data: pd.DataFrame)
Displays a detailed list of vocabulary with progress information.
- Clears previous content
- Creates headers for the list
- For each word, displays:
  - Word in target language with translation
  - Success rate with number of attempts
  - Learning status indicator with color coding

## Learning Status Categories
Words are categorized with visual indicators:
- **Learnt** (Green): Words that meet the minimum practice count and success rate criteria
- **In Progress** (Orange): Words with some practice and moderate success rate (≥60%)
- **Needs Practice** (Red): Words with practice but low success rate (<60%)
- **Not Started**: Words that have not been practiced yet

## Color Coding
- **Green**: Words that meet learning criteria
- **Orange**: Words with good progress but not yet fully learned
- **Red**: Words that need additional practice

## Statistics Display
The view calculates and displays:
- Total number of words in vocabulary
- Number of words meeting learning criteria
- Number of words partially learned (practiced but not fully learned)
- Average success rate across all practiced words

## Learning Criteria
The criteria for considering a word "learnt" are displayed and based on user settings:
- Minimum number of practice attempts
- Minimum success rate (percentage)

## Navigation
- "Continue Learning" button returns to the main learning flow
