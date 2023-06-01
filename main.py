from src.openai_scripts import call_whisper, call_gpt
from src.data_scripts import (
    append_to_or_create_txt_file,
    open_txt_file,
    insert_newlines,
    backup_data,
)

from dotenv import load_dotenv
import os


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

summary_prompt = "Summarize the following text:"

mp3_path = "data/voice_message.mp3"
desired_txt_path = "data/summarized_mp3.txt"


def main():
    # transcribe mp3
    transcription = call_whisper(
        api_key=OPENAI_API_KEY,
        action="transcribe",
        mp3_path=mp3_path,
    )

    summary = call_gpt(
        api_key=OPENAI_API_KEY, prompt=summary_prompt, input_text=transcription
    )

    summary = backup_data(
        input_data=summary, input_name="voice_summary", backup_directory="data"
    )
    summary_formatted = insert_newlines(string=summary, every=96)

    print(f"\n{summary_formatted}\n")


# Run the main function
if __name__ == "__main__":
    main()
