Notepad Application with Advanced Text Processing

Overview

This is a Python-based text editor built with the Tkinter library, featuring advanced functionalities like speech-to-text conversion, spell checking, word filtering, and text-to-speech. Additionally, it includes typical notepad operations such as opening, saving, and editing text files.

Features

Basic Notepad Operations:
Create, open, save, and edit text files.
Cut, copy, and paste functionalities.
Spell Checking:
Highlights misspelled words and suggests possible corrections.
Speech to Text:
Converts speech input to text using the Google Speech Recognition API.
Text to Speech:
Reads aloud text using Google Text-to-Speech (gTTS).
Find and Replace:
Search for specific words in the document and replace them.
Bad Word Filtering:
Detects and highlights words matching a list of bad words (stored in badwords.txt).
Requirements

The following libraries are required to run the application:

tkinter
fuzzywuzzy
gTTS
spellchecker
SpeechRecognition
pyttsx3
Install the required packages using the following command:

bash
Copy code
pip install tkinter fuzzywuzzy gTTS pyspellchecker SpeechRecognition pyttsx3
How to Run

Clone or download the repository.
Install the necessary dependencies (see Requirements section).
Run the application by executing the Python script:
bash
Copy code
python notepad.py
How to Use

Text Operations:
Open the application and type or paste your text.
Use the file menu to create, open, save, or exit files.
Spell Checking:
To check spelling, right-click on a highlighted word and select "Show all Possible Words" for suggestions, or select "Correct Word" to auto-correct.
Speech to Text:
Start speaking and the text will automatically appear in the notepad.
Text to Speech:
Click the read button to have the content read aloud using Google Text-to-Speech.
Find and Replace:
Search for a word or phrase using the "Search" button or use the "Replace" button to replace specific text.
Filter Bad Words:
Bad words from the badwords.txt file will be highlighted in blue.
Notes

For the speech-to-text functionality, an internet connection is required since it uses Google's Speech Recognition API.
If gTTS does not work on your system, you may need to configure your audio settings or change the command in the os.system("start Hello.mp3") line to suit your operating system.
