import pyttsx3
import re
import openai
import tkinter as tk

# Constants
MODEL_NAME = "gpt-3.5-turbo"
API_KEY = "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"  # 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
VOICE_MAPPING = {
    "Zira": 0,
    "Hazel": 1
}
RE_STAGE_DIRECTIONS = re.compile(r'\([^)]*\)|\[.*?\]|\*.*?\*')

# Initialize OpenAI API key
openai.api_key = API_KEY

# Set up pyttsx3 engine and configure it only once
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Initialize the subtitle window
root = tk.Tk()
root.attributes('-transparentcolor', 'black')
root.overrideredirect(True)
root.lift()
root.wm_attributes("-topmost", True)
root.wm_attributes("-disabled", True)
subtitle_width = 1100
label = tk.Label(root, text='', font=('Helvetica', 30), fg='white', bg='black', wraplength=subtitle_width, justify='center')
label.pack()

def main():
    global MODEL_NAME
    print_intro()
    # Let the user choose the model
    model_choice = input("Choose the AI model (1 for GPT-3.5-turbo, 2 for GPT-4): ").strip()
    if model_choice == "2":
        MODEL_NAME = "gpt-4"
    else:
        MODEL_NAME = "gpt-3.5-turbo"

    init_subtitle_window()  # Initialize the subtitle window
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


def print_intro():
    intro = (
        "Welcome to another exciting episode of 'Zira & Hazel'! Get ready to dive into the hilarious world of two roommates with contrasting personalities. "
        "Zira, the assertive American, and Hazel, the sarcastic Brit, keep us entertained with their witty exchanges. Let's start the show!\n"
    )
    print(intro)

def handle_episode(episode_number):
    topic = input(f"Enter the topic for episode {episode_number}: ")
    print("Preparing episode...\n")

    conversation = prepare_conversation(episode_number, topic)
    response = openai.ChatCompletion.create(model=MODEL_NAME, messages=conversation)
    dialogue = remove_stage_directions(response.choices[0].message['content'])

    print("\nScript written. Time to roll!\n")
    speak_dialogue(dialogue)

def prepare_conversation(episode_number, topic):
    return [
        {"role": "system", "content": "You are to craft a humorous dialogue showcasing the contrasting personalities of Zira and Hazel, who are roommates. Zira, an assertive, outspoken American, "
                                             "often dominates conversations with her audacious demands, while British Hazel, trying to be easy-going and kind-hearted, responds with sarcastic retorts or barely "
                                             "concealed annoyance. Your dialogue should be lively and authentic, reflecting the dynamics between two friends who cherish yet irk each other. "
                                             "The script should be written in the following format: \"Zira: <dialogue> Hazel: <dialogue>\", with each new line of dialogue not necessarily alternating between characters. "
                                             "Refrain from including stage directions or any elements beyond the speaker's name and dialogue. The conversation should revolve around a user-provided topic."},
                {"role": "user", "content": f"Write episode {episode_number} about: {topic}"}
    ]

def speak_dialogue(dialogue):
    for line in dialogue.split('\n'):
        if line:
            speaker, line_dialogue = line.split(': ', 1)
            set_voice(speaker)
            update_subtitle(f"{speaker}: {line_dialogue}")
            engine.say(line_dialogue)
            engine.runAndWait()
    update_subtitle("")  # Clear the subtitle after speaking

def set_voice(speaker):
    voice_index = VOICE_MAPPING.get(speaker)
    if voice_index is not None:
        engine.setProperty('voice', voices[voice_index].id)

def remove_stage_directions(text):
    return RE_STAGE_DIRECTIONS.sub('', text)

def init_subtitle_window():
    global root, label
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    label.update_idletasks()
    window_width = subtitle_width
    window_height = label.winfo_reqheight()
    x_coordinate = (screen_width // 2) - (window_width // 2)
    y_coordinate = screen_height - window_height - 125 # Adjust the vertical position of the subtitle
    root.geometry(f"+{x_coordinate}+{y_coordinate}")

def update_subtitle(text):
    label.config(text=text)
    root.update_idletasks()
    root.update()

if __name__ == "__main__":
    main()
    root.mainloop()  # Start the Tkinter event loop
