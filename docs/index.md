# Polyglot Documentation

Welcome to the Polyglot language learning application documentation.

## About Polyglot

Polyglot is an interactive language learning application built with Python and customtkinter. It provides a personalized learning experience with AI-powered vocabulary generation, flashcards, knowledge testing, and progress tracking.

## Documentation Structure

This documentation is organized into the following sections:

### Application Components

- [Views](views/index.md): UI components that present the application to the user
- Controllers: Business logic components that manage application state and operations
- Services: External service integrations and utilities

### Mental Models

- [Mental Model](mental_model.md): Conceptual overview of how Polyglot works
- [Implementation Details](implementation_details.md): Technical implementation specifics
- [Gotchas](gotchas.md): Common pitfalls and edge cases
- [Quick Reference](quick_reference.md): Key parameters and configurations

## Key Features

Polyglot offers the following features:

1. **Personalized Learning**:
   - User-selected language pairs
   - Customizable proficiency level
   - Topic selection for vocabulary focus

2. **Vocabulary Management**:
   - AI-powered vocabulary generation
   - Custom word addition
   - Spaced repetition learning algorithm

3. **Interactive Learning**:
   - Flashcards with translations and examples
   - Translation tests with multiple choice options
   - Sentence context exercises
   - Full sentence translation practice with AI feedback

4. **Progress Tracking**:
   - Word mastery statistics
   - Learning progress visualization
   - Adaptive learning based on performance

## Technical Overview

Polyglot follows a Model-View-Controller (MVC) architecture:

- **Models**: Data structures representing vocabulary, user settings, and learning progress
- **Views**: User interface components for interaction
- **Controllers**: Business logic components managing the application state

The application uses:
- Python 3.13+
- customtkinter for UI components
- OpenAI API for vocabulary generation
- CSV files for data storage

## Getting Started

For installation and setup instructions, see the [README.md](../README.md) file in the project root.

## Contributing

When contributing to Polyglot, please follow these principles:

1. **Documentation First**: Always review and update documentation when making changes
2. **Preserve Functionality**: Avoid removing or modifying existing features without explicit permission
3. **Documentation Maintenance**: Keep documentation up-to-date with code changes
4. **Follow Change Management**: Propose changes with clear rationale and get approval before implementation
