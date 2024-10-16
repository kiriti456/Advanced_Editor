# Notepad Application with Advanced Text Processing

## Overview

This is a Python-based text editor built with the **Tkinter** library, featuring advanced functionalities like speech-to-text conversion, spell checking, word filtering, and text-to-speech. Additionally, it includes typical notepad operations such as opening, saving, and editing text files.

## Features

- **Basic Notepad Operations:**
  - Create, open, save, and edit text files.
  - Cut, copy, and paste functionalities.
  
- **Spell Checking:**
  - Highlights misspelled words and suggests possible corrections.

- **Speech to Text:**
  - Converts speech input to text using the Google Speech Recognition API.

- **Text to Speech:**
  - Reads aloud text using Google Text-to-Speech (gTTS).

- **Find and Replace:**
  - Search for specific words in the document and replace them.

- **Bad Word Filtering:**
  - Detects and highlights words matching a list of bad words (stored in `badwords.txt`).

## Requirements

The following libraries are required to run the application:
- `tkinter`
- `fuzzywuzzy`
- `gTTS`
- `spellchecker`
- `SpeechRecognition`
- `pyttsx3`

Install the required packages using the following command:
```bash
pip install tkinter fuzzywuzzy gTTS pyspellchecker SpeechRecognition pyttsx3
