import os
import re
import tkinter as tk
import pyttsx3
from groq import Groq
from typing import Dict, List

# Constants
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("API key for Groq is not set in environment variables.")

VOICE_MAPPING: Dict[str, int] = {
    "Zira": 0,
    "Hazel": 1
}
RE_STAGE_DIRECTIONS = re.compile(r'\([^)]*\)|\[.*?\]|\*.*?\*')
SUBTITLE_WIDTH = 1100
SUBTITLE_FONT = ('Helvetica', 30)

# Initialize Groq client, pyttsx3 engine, and Tkinter window
client = Groq(api_key=API_KEY)
engine = pyttsx3.init()
voices = engine.getProperty('voices')

root = tk.Tk()
label = tk.Label(root, text='', font=SUBTITLE_FONT, fg='white', bg='black', wraplength=SUBTITLE_WIDTH, justify='center')
label.pack()

def init_subtitle_window() -> None:
    root.attributes('-transparentcolor', 'black')
    root.overrideredirect(True)
    root.lift()
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-disabled", True)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    label.update_idletasks()
    window_height = label.winfo_reqheight()
    x_coordinate = (screen_width - SUBTITLE_WIDTH) // 2
    y_coordinate = screen_height - window_height - 140
    root.geometry(f"+{x_coordinate}+{y_coordinate}")

def update_subtitle(text: str) -> None:
    label.config(text=text)
    root.update_idletasks()

def print_intro() -> None:
    intro = (
        "Welcome to another exciting episode of 'Zira & Hazel'! Get ready to dive into the hilarious world of two roommates with contrasting personalities. "
        "Zira, the assertive American, and Hazel, the sarcastic Brit, keep us entertained with their witty exchanges. Let's start the show!\n"
    )
    print(intro)

def prepare_conversation(episode_number: int, topic: str) -> List[Dict[str, str]]:
    return [
        {"role": "system", "content": "You are to craft a humorous dialogue showcasing the contrasting personalities of Zira and Hazel, who are roommates. Zira, an assertive, outspoken American, "
                                      "often dominates conversations with her audacious demands, while British Hazel, trying to be easy-going and kind-hearted, responds with sarcastic retorts or barely "
                                      "concealed annoyance. Your dialogue should be lively and authentic, reflecting the dynamics between two friends who cherish yet irk each other. "
                                      "The script should be written in the following format: \"Zira: <dialogue> Hazel: <dialogue>\", with each new line of dialogue not necessarily alternating between characters. "
                                      "Refrain from including stage directions or any elements beyond the speaker's name and dialogue. The conversation should revolve around a user-provided topic."},
        {"role": "user", "content": f"Write episode {episode_number} about: {topic}"}
    ]

def remove_stage_directions(text: str) -> str:
    return RE_STAGE_DIRECTIONS.sub('', text)

def set_voice(speaker: str) -> None:
    voice_index = VOICE_MAPPING.get(speaker)
    if voice_index is not None:
        engine.setProperty('voice', voices[voice_index].id)

def speak_dialogue(dialogue: str) -> None:
    for line in dialogue.split('\n'):
        if line:
            speaker, line_dialogue = line.split(': ', 1)
            set_voice(speaker)
            update_subtitle(f"{speaker}: {line_dialogue}")
            engine.say(line_dialogue)
            engine.runAndWait()
    update_subtitle("")  # Clear the subtitle after speaking

def handle_episode(episode_number: int) -> None:
    topic = input(f"Enter the topic for episode {episode_number}: ")
    print("Preparing episode...\n")

    conversation = prepare_conversation(episode_number, topic)
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=conversation,
        temperature=1,
        max_tokens=8000,
        top_p=1,
        stream=False  # Set to False to get the entire response at once
    )
    dialogue = remove_stage_directions(response.choices[0].message.content)  # Extract the generated text

    print("\nScript written. Time to roll!\n")
    speak_dialogue(dialogue)

def main() -> None:
    print_intro()
    init_subtitle_window()

    episode_number = 1
    try:
        while True:
            handle_episode(episode_number)
            episode_number += 1
    except KeyboardInterrupt:
        print("Program terminated by the user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        root.destroy()  # Ensure the Tkinter window is closed when the program ends

if __name__ == "__main__":
    main()
    root.mainloop()  # Start the Tkinter event loop
