# Polyglot - Language Learning Application

A modern and interactive language learning application built with Python and customtkinter. Learn new vocabulary through flashcards, test your knowledge, and track your progress.

## Features

- Personalized learning experience based on your language preferences and level
- AI-powered vocabulary generation using OpenAI
- Interactive flashcards with translations and example sentences
- Knowledge testing with multiple choice and typing exercises
- Progress tracking and statistics
- Configurable learning settings

## Requirements

- Python 3.13
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/polyglot.git
cd polyglot
```

2. Install system dependencies:
```bash
# For Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.XX-tk

# For Fedora
sudo dnf install python3-tkinter

# For Arch Linux
sudo pacman -S tk
```

3. Install Python dependencies:
```bash
# If you don't have uv installed
pip install uv

# Install dependencies using uv
uv venv
source .venv/bin/activate  # On Linux/macOS
uv sync
```

4. Set up your OpenAI API key:
Create a `.env` file in the project root and add your API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run the application:
```bash
python -m polyglot.app
```

## Configuration

You can customize your learning experience through the settings menu:
- Words per day (default: 5)
- Flashcard display duration (default: 5 seconds)
- Number of words per test (default: 10)

## Data Storage

The application stores your data in the following locations:
- User settings: `~/.polyglot/user_settings.json`
- Vocabulary: `~/.polyglot/vocabulary.csv`
