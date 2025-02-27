# Polyglot Views Documentation

This documentation provides detailed information about the views in the Polyglot language learning application.

## Overview

Polyglot's user interface is organized into a series of view classes, each responsible for a specific aspect of the application's functionality. These views are implemented as customtkinter frames and are managed by the application's main controller.

## View Structure

The views follow a consistent pattern:
- Each view extends `ctk.CTkFrame`
- Views receive necessary controllers as dependencies
- Views include an `on_complete` callback for navigation
- UI components are created in a `setup_ui()` method

## Available Views

| View | Description | Primary Function |
|------|-------------|------------------|
| [MenuView](menu_view.md) | Main navigation hub | Provides access to all app features |
| [OnboardingView](onboarding_view.md) | User setup wizard | Collects user preferences for initial setup |
| [FlashcardView](flashcard_view.md) | Vocabulary learning | Displays daily words as interactive flashcards |
| [TestView](test_view.md) | Translation testing | Tests word translation knowledge |
| [SentenceTestView](sentence_test_view.md) | Context practice | Practices words in sentence context |
| [SentenceTranslationView](sentence_translation_view.md) | Translation practice | Practices full sentence translations with LLM feedback |
| [ProgressView](progress_view.md) | Statistics display | Shows vocabulary learning progress |
| [AddWordView](add_word_view.md) | Vocabulary management | Allows adding custom vocabulary |
| [SettingsView](settings_view.md) | Configuration | Adjusts application settings |

## Navigation Flow

The typical user flow through the views is:
1. New users start with **OnboardingView** to set preferences
2. **MenuView** serves as the central hub for all features
3. **FlashcardView** presents daily vocabulary for learning
4. **TestView** tests translation knowledge
5. **SentenceTestView** tests contextual usage
6. **SentenceTranslationView** practices full sentence translations
7. **ProgressView** shows learning statistics

## UI Components

The views use the following common UI components:
- Labels for displaying text
- Buttons for actions
- Frames for organizing content
- Entry fields for text input
- Scrollable frames for displaying lists

## Controller Dependencies

Views interact with these controllers:
- **VocabularyController**: Manages vocabulary and learning algorithms
- **UserController**: Manages user settings and preferences

## Extending Views

When implementing new views:
1. Follow the established pattern
2. Ensure consistent UI styling
3. Implement proper navigation callbacks
4. Handle appropriate error cases

For more detailed information, see the documentation for each specific view.
