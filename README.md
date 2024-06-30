# Nike Air Jordan Collection Chatbot

## Overview

This project is an AI-powered chatbot that assists customers in accessing product-related information from the Nike Air Jordan collection. It uses text information from the website and image data from product photos to help users find merchandise based on their preferences. The chatbot supports text queries, image queries, and voice queries.

## Project Structure

- **main.py**: The main script to run the chatbot interface.
- **.env**: Environment file containing API keys.
- **requirements.txt**: List of dependencies required for the project.
- **README.md**: Documentation of the project.
- **utils/**: Directory containing utility modules.
  - **__init__.py**: Initializes the utils package.
  - **image_processing.py**: Functions for image processing.
  - **openai_api.py**: Functions for interacting with OpenAI API.
  - **speech_recognition.py**: Functions for speech recognition.
  - **text_to_speech.py**: Functions for converting text to speech.
  - **web_scraping.py**: Functions for web scraping.

## Setup

### Prerequisites

- Python 3.x
- Virtual environment tools (optional but recommended)

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/nike-air-jordan-chatbot.git
   cd nike-air-jordan-chatbot
   ```

2. **Create a virtual environment and activate it:**
   ```sh
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install the required dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Create a `.env` file and add your OpenAI API key:**
   ```sh
   echo "OPENAI_API_KEY=your_openai_api_key" > .env
   ```

### Dependencies

Make sure you have the following dependencies listed in your `requirements.txt` file:

```
requests
beautifulsoup4
openai
python-dotenv
Pillow
gtts
pygame
easygui
SpeechRecognition
pydub
```

### Usage

Run the chatbot:

```sh
python main.py
```