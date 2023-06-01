# OpenAI Whisper + GPT-3

This project performs speech-to-text transcription and text summarization using OpenAI's APIs.
One use-case can be the summarizing of long voice messages.

## Prerequisites

- Python 3.6 or higher
- `python-dotenv` package
- OpenAI API key

## Installation

1. Clone the repository:
`git clone https://github.com/your-username/your-repo.git`

2. Navigate to the project directory:
`cd your-repo`

3. Create a virtual environment (optional): `python -m venv venv`

4. Activate the virtual environment (optional):

    - On macOS and Linux: `source venv/bin/activate`

    - On Windows: `./venv/Scripts/activate`


5. Install the required packages:
`pip install -r requirements.txt`


## Configuration

1. Create a `.env` file in the root directory of the project.

2. Add your OpenAI API key to the `.env` file:
`OPENAI_API_KEY=your-api-key`

## Usage

1. Place your .mp3 file in the `data` directory with the name `voice_message.mp3`.

2. Run the main script:
`python main.py`


3. The script will transcribe the mp3 file, summarize the transcription using OpenAI's GPT model, and save the summarized text in a file named `summarized_mp3.txt` in the `data` directory.

4. The summarized text will be printed on the console.
---
## License

This project is licensed under the [MIT License](LICENSE).
