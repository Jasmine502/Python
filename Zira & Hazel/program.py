import pyttsx3
import re
import openai
import os
from dotenv import load_dotenv

# Load environmental variables from .env file
load_dotenv()

# Set up pyttsx3 engine
engine = pyttsx3.init()

# Constants
MODEL_NAME = "gpt-3.5-turbo"

# Voice mapping dictionary
VOICE_MAPPING = {
    "Zira": 0,
    "Hazel": 1
}

def main():
    try:
        check_api_key()

        print_intro()

        episode_number = 1
        while True:
            topic = input(f"Enter the topic for episode {episode_number}: ")
            print("Preparing episode...\n")

            # Prepare conversation structure
            conversation = [
                {"role": "system", "content": "You are to craft a humorous dialogue showcasing the contrasting personalities of Zira and Hazel, who are roommates. Zira, an assertive, outspoken American, "
                                             "often dominates conversations with her audacious demands, while British Hazel, trying to be easy-going and kind-hearted, responds with sarcastic retorts or barely "
                                             "concealed annoyance. Your dialogue should be lively and authentic, reflecting the dynamics between two friends who cherish yet irk each other. "
                                             "The script should be written in the following format: \"Zira: <dialogue> Hazel: <dialogue>\", with each new line of dialogue not necessarily alternating between characters. "
                                             "Refrain from including stage directions or any elements beyond the speaker's name and dialogue. The conversation should revolve around a user-provided topic."},
                {"role": "user", "content": f"Write episode {episode_number} about: {topic}"}
            ]

            response = openai.ChatCompletion.create(
                model=MODEL_NAME,
                messages=conversation
            )

            dialogue = response.choices[0].message['content']
            dialogue = remove_stage_directions(dialogue)  # Remove stage directions

            # Save dialogue to script file
            with open('script.txt', 'w') as f:
                f.write(dialogue)

            print("\nScript written. Time to roll!\n")

            # Speak dialogue from the script with subtitles
            with open('script.txt') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split(': ', 1)
                        if len(parts) == 2:
                            speaker, dialogue = parts
                            speak_dialogue(speaker, dialogue)
                        else:
                            print(line)
                print("\n" + "-" * 40)

            episode_number += 1

    except Exception as e:
        print("An error occurred:", str(e))

def check_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None or api_key.strip() == "":
        while True:
            api_key = input("No API key detected. Please enter your OpenAI API key: ").strip()
            if api_key:
                save_api_key(api_key)
                openai.api_key = api_key
                break
            else:
                print("API key cannot be empty. Please try again.")
    else:
        openai.api_key = api_key

def save_api_key(api_key):
    with open('.env', 'a') as f:
        f.write(f"OPENAI_API_KEY={api_key}\n")

def print_intro():
    intro = (
        "Welcome to another exciting episode of 'Zira & Hazel'! Get ready to dive into the hilarious world of two roommates with contrasting personalities. "
        "Zira, the assertive American, and Hazel, the sarcastic Brit, keep us entertained with their witty exchanges. Let's start the show!\n"
    )
    print(intro)

def speak_dialogue(speaker, dialogue):
    voices = engine.getProperty('voices')

    if speaker in VOICE_MAPPING:
        voice_index = VOICE_MAPPING[speaker]
        target_voice = voices[voice_index]
        engine.setProperty('voice', target_voice.id)

    print(f"\n{speaker}: {dialogue}")  # Print subtitles
    engine.say(dialogue)
    engine.runAndWait()

def remove_stage_directions(text):
    # Remove stage directions enclosed in brackets or asterisks
    text = re.sub(r'\([^)]*\)', '', text)    # Remove anything inside parentheses
    text = re.sub(r'\[.*?\]', '', text)      # Remove anything inside square brackets
    text = re.sub(r'\*.*?\*', '', text)      # Remove anything inside asterisks
    return text

if __name__ == "__main__":
    main()
