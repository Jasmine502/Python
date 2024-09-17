import os
import random
from groq import Groq
import tkinter as tk
from tkinter import font
import pygame  # Import pygame for sound

# Initialize the Groq client with API key from environment variable
api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    raise ValueError("API key not found. Please set the GROQ_API_KEY environment variable.")
client = Groq(api_key=api_key)

# Global variable for initial window size
global initial_window_size
initial_window_size = None

# Function to read Minecraft items from the text file
def read_items(file_path):
    with open(file_path, 'r') as file:
        return [item.strip().lower() for item in file]

# Function to interact with the Groq API
def generate_combined_item(item1, item2):
    prompt = f"""Assume the role of a Minecraft API. Your task is to analyze a pair of items and predict a plausible single item that could result from their combination. Present the output in the following format:


Item name, MUST be the FIRST LINE of the message,  with NO PUNCTUATION or SYMBOLS, and must be an appropriate name that sounds like it would be in the game.
- Type: [General category (Natural, Wood, Mob Drops, Food, Stone, Colorful, Combat, Minerals, Tools, Mining, Brewing, Nether, End, Mechanism, Miscellaneous, Magic Items, Mass Junk, Other Junk, Trophy Items)]
- Description: [Brief function or purpose]
- Durability: [For tools, weapons, armor; if applicable]
- Stack Size: [Max items in a single inventory slot]
- Rarity: [Item's commonality]
- Enchantments: [Possible enchantments that exist in the game; if applicable]

- Crafting Recipe: [Ingredients and crafting table arrangement; if craftable]
- Obtaining: [Acquisition methods, no events]
- Usage: [Specific applications]
- Effects: [Special effects when used/equipped]

DO NOT ADD ANY MORE TEXT AFTER EFFECTS
Note: Feel free to invent new items not present in the standard Minecraft game. Prioritize logical and creative combinations, considering the input items' properties and the Minecraft universe's potential. If the combination doesn't yield a clear result, provide an explanation or suggest alternative outcomes."""

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f'Input: "{item1}" + "{item2}"'
            }
        ],
        temperature=1,
        max_tokens=2000,
        top_p=1,
        stream=False,  # Set to False to get the entire response at once
        stop=None,
    )

    return completion.choices[0].message.content

# Function to handle the "Generate" button click
def generate_item():
    global initial_window_size
    play_sound()  # Play sound on button click
    item1 = item1_entry.get().strip().lower()
    item2 = item2_entry.get().strip().lower()

    if not initial_window_size:
        initial_window_size = root.geometry()

    if not item1 and not item2:
        item1, item2 = random.sample(items, 2)
        item1_entry.insert(0, item1)
        item2_entry.insert(0, item2)
        result_label.config(text=f"Randomly selected items: {item1}, {item2}")
    elif not item1:
        item1 = random.choice(items)
        item1_entry.insert(0, item1)
        result_label.config(text=f"Randomly selected item for the first slot: {item1}")
    elif not item2:
        item2 = random.choice(items)
        item2_entry.insert(0, item2)
        result_label.config(text=f"Randomly selected item for the second slot: {item2}")
    else:
        if item1 not in items or item2 not in items:
            result_label.config(text="One or both items are not valid. Please try again.")
            return

        result = generate_combined_item(item1, item2)
        result_label.config(text=result, justify="left")  # Align text to the left

        # Update window width based on generated text
        result_label.update_idletasks()  # Force label to update its size
        width = result_label.winfo_width() + 20  # Add some padding
        root.geometry(f"{width}x{root.winfo_height()}")  # Update only the width

# Function to clear the entry fields
def clear_fields():
    global initial_window_size
    play_sound()  # Play sound on button click
    item1_entry.delete(0, tk.END)
    item2_entry.delete(0, tk.END)
    result_label.config(text="")

    if initial_window_size:
        root.geometry(initial_window_size)

# Function to play the sound effect
def play_sound():
    pygame.mixer.init()  # Initialize pygame mixer
    pygame.mixer.music.play()  # Play the sound

# Create the main window
root = tk.Tk()
root.title("Minecraft Infinite Craft")
root.configure(bg="#333333")  # Dark gray background

# Set Minecraft font
minecraft_font = font.Font(family="Minecraft", size=12)

# Create labels and entry fields for item names
item1_label = tk.Label(root, text="Item 1:", font=minecraft_font, bg="#333333", fg="white")
item1_label.grid(row=0, column=0, padx=5, pady=5)
item1_entry = tk.Entry(root, font=minecraft_font, bg="#444444", fg="white", relief="solid", borderwidth=2)
item1_entry.grid(row=0, column=1, padx=5, pady=5)

item2_label = tk.Label(root, text="Item 2:", font=minecraft_font, bg="#333333", fg="white")
item2_label.grid(row=1, column=0, padx=5, pady=5)
item2_entry = tk.Entry(root, font=minecraft_font, bg="#444444", fg="white", relief="solid", borderwidth=2)
item2_entry.grid(row=1, column=1, padx=5, pady=5)

# Create the "Generate" button
generate_button = tk.Button(root, text="Generate", command=generate_item, font=minecraft_font, bg="#555555", fg="white", relief="solid", borderwidth=2)
generate_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)  # Centered

# Create the "Clear" button
clear_button = tk.Button(root, text="Clear", command=clear_fields, font=minecraft_font, bg="#555555", fg="white", relief="solid", borderwidth=2)
clear_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)  # Right below Generate

# Create a label to display the generated item details
result_label = tk.Label(root, text="", wraplength=400, justify="left", font=minecraft_font, bg="#333333", fg="white")  # Align text to the left
result_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Read items from the text file
file_path = os.path.join(script_dir, "items.txt")
items = read_items(file_path)

# Initialize pygame and load sound
pygame.mixer.init()
sound_file = os.path.join(script_dir, "Click_stereo.mp3")
pygame.mixer.music.load(sound_file)

# Run the main loop
root.mainloop()
