import openai
import time
import requests


def call_gpt(api_key, prompt, input_text="", model=None):
    # Set your OpenAI API key
    openai.api_key = api_key

    if prompt == None:
        prompt = input("No prompt specified. What do you want ChatGPT to do?\nPrompt: ")

    if model == None:
        model = "gpt-3.5-turbo"

    # Concatenate the prompt and input input_text
    full_prompt = prompt + str(input_text)

    attempts = 0
    while attempts < 5:
        try:
            # Send the request to the Chat API
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": full_prompt},
                ],
            )

            # Extract the generated summary from the API response
            output_text = response.choices[0].message.content

            # print(f"\n{output_text}")
            print(f"Successfully called {model} from the OpenAI API.")
            return output_text

        except (openai.error.RateLimitError, requests.exceptions.ConnectionError):
            print(
                f"ERROR encountered. New API call attempt in {(2**attempts)} seconds...\n"
            )
            time.sleep((2**attempts))
            attempts += 1


def call_whisper(api_key, action, mp3_path):
    """
    Could need some love regarding other whisper functions
    and the opening of any kind of path format or taking a
    prompt as specified in the OpenAI API docs:
    https://platform.openai.com/docs/guides/speech-to-text/longer-inputs

    """

    openai.api_key = api_key

    audio_file = open(
        rf"{mp3_path}",
        "rb",
    )

    if action == "transcribe".casefold():
        api_result = openai.Audio.transcribe("whisper-1", audio_file)["text"]
        if api_result != None:
            print(
                f"Successfully called the whisper model to {action} from the OpenAI API."
            )
            return api_result
        else:
            return "Something failed and the API result is None."
    else:
        return "Wrongly specified action. Try again."
