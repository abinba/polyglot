# Polyglot Mental Model

This document provides a conceptual overview of how Polyglot works, explaining the core concepts and relationships between components.

## Core Concepts

### Language Learning Process

Polyglot follows a structured language learning process:

1. **Vocabulary Acquisition**: Users learn new words through flashcards
2. **Knowledge Testing**: Users test their knowledge through translation exercises
3. **Contextual Understanding**: Users practice using words in sentences
4. **Progress Review**: Users track their learning progress and statistics

### Spaced Repetition

Polyglot uses a spaced repetition system to optimize learning:

1. Words are initially presented at short intervals
2. As mastery increases, intervals between reviews increase
3. Words with low success rates are presented more frequently
4. Words meeting learning criteria (practice count and success rate) are considered learned

### Learning Progression

The application guides users through a natural learning progression:

1. **Onboarding**: Setup language preferences and learning goals
2. **Daily Learning**: Review new vocabulary with translations and examples
3. **Testing**: Verify knowledge through multiple-choice tests
4. **Context Practice**: Apply knowledge in sentence contexts
5. **Translation Practice**: Translate complete sentences with LLM-powered feedback
6. **Review**: Track progress and identify areas for improvement

## Component Relationships

### User Settings → Vocabulary Generation

User preferences (language pair, level, topics) directly influence the vocabulary generated:
- Native language determines translations
- Target language determines vocabulary words
- Proficiency level determines word difficulty
- Selected topics determine the semantic domains of words

### Vocabulary → Learning Activities

The vocabulary database drives all learning activities:
- Flashcards display words with translations and examples
- Tests generate questions based on the vocabulary
- Sentence exercises use words in context
- Progress tracking measures mastery of vocabulary items

### User Performance → Learning Algorithm

User performance in tests and exercises influences the learning algorithm:
- Correct answers increase a word's mastery level
- Incorrect answers decrease a word's mastery level
- Words with lower mastery levels appear more frequently
- Learning statistics guide the selection of words for testing

## Mental Map

```
┌─────────────────┐       ┌───────────────────┐       ┌────────────────┐
│  User Settings  │──────▶│ Vocabulary System │──────▶│ Learning Views │
└─────────────────┘       └───────────────────┘       └────────────────┘
        ▲                          │                          │
        │                          │                          │
        └──────────────────────────┴──────────────────────────┘
                             Performance Data
```

This cyclic relationship creates a personalized learning experience that adapts to the user's performance and preferences, optimizing the language learning process.

## Next Steps

For technical implementation details of these concepts, see [Implementation Details](implementation_details.md).
