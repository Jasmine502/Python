import os
import re
import pyttsx3
from groq import Groq
from typing import Dict, List

# Constants
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("API key for Groq is not set in environment variables.")

VOICE_MAPPING: Dict[str, int] = {
    "FOR": 0,
    "AGAINST": 1
}
RE_STAGE_DIRECTIONS = re.compile(r'\([^)]*\)|\[.*?\]|\*.*?\*')

# Initialize Groq client and pyttsx3 engine
client = Groq(api_key=API_KEY)
engine = pyttsx3.init()
voices = engine.getProperty('voices')

def print_intro() -> None:
    intro = (
        "Welcome to the AI Debate Generator! Get ready to witness a clash of perspectives. "
        "Two AI agents will engage in a heated debate on a topic of your choice. Let the debate begin!\n"
    )
    print(intro)

def prepare_debate(topic: str) -> List[Dict[str, str]]:
    content = (
        f"Your task is to facilitate a structured debate between two AI agents, "
        f"one named 'Forrest' representing the 'FOR' side and the other named 'Agatha' "
        f"representing the 'AGAINST' side of a given topic. Each agent will present "
        f"their arguments and rebuttals in a persuasive manner, with each argument and "
        f"rebuttal being at least 2 paragraphs long. The debate will follow this format: "
        f"Forrest presents the initial argument, Agatha rebuts and presents her own argument, "
        f"Forrest rebuts and presents a new argument, and so on. The debate will continue until "
        f"a natural conclusion is reached. Each line of dialogue should begin with either 'FOR:' "
        f"or 'AGAINST:', followed by a space and then the argument. No other prefixes or formats "
        f"are allowed. The topic for this debate is {topic}."
    )
    return [{"role": "system", "content": content}]

def remove_stage_directions(text: str) -> str:
    return RE_STAGE_DIRECTIONS.sub('', text)

def set_voice(speaker: str) -> None:
    voice_index = VOICE_MAPPING.get(speaker)
    if voice_index is not None:
        engine.setProperty('voice', voices[voice_index].id)

def print_and_speak(speaker: str, line_debate: str) -> None:
    """Prints and speaks the debate line in a formatted manner."""
    formatted_line = f"{speaker}: {line_debate}\n"
    print(formatted_line)  # Print to console
    engine.say(line_debate)
    engine.runAndWait()

def speak_debate(debate: str) -> None:
    for line in debate.split('\n'):
        if line and ': ' in line:
            speaker, line_debate = line.split(': ', 1)
            set_voice(speaker)
            print_and_speak(speaker, line_debate)  # Use the new helper function
        else:
            print(f"Skipping malformed line: {line}")

def handle_debate() -> None:
    topic = input("Enter the debate topic: ")

    print("Preparing the debate...\n")

    conversation = prepare_debate(topic)
    conversation_history = []  # Initialize conversation history

    # Start the debate loop
    while True:
        # FOR AI's turn
        response_for = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=conversation + conversation_history + [{"role": "user", "content": "FOR:"}],
            temperature=0.7,
            max_tokens=8000,
            top_p=1,
            stream=False
        )
        for_argument = response_for.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": for_argument})

        # Print and speak FOR AI's argument
        print_and_speak("FOR", for_argument)

        # AGAINST AI's turn
        response_against = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=conversation + conversation_history + [{"role": "user", "content": "AGAINST:"}],
            temperature=0.7,
            max_tokens=8000,
            top_p=1,
            stream=False
        )
        against_argument = response_against.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": against_argument})

        # Print and speak AGAINST AI's argument
        print_and_speak("AGAINST", against_argument)

        # Check for a natural conclusion (you can implement your own logic here)
        if len(conversation_history) >= 10:  # Example condition to end the debate
            print("Debate has reached a natural conclusion.")
            break

def main() -> None:
    print_intro()

    try:
        while True:
            handle_debate()
    except KeyboardInterrupt:
        print("Program terminated by the user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()