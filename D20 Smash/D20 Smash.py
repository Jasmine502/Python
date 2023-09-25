# Import modules
import random
import pyttsx3
import time

# Constants
PENALTIES_FILE = "penalties.txt"
ADVANTAGES_FILE = "advantages.txt"
YOU_SD_PENALTY = "SEPPUKU: YOU SD 2 STOCKS"
YOU_PICK_DICE_PENALTY = "YOU DECIDE: YOU PICK OPPONENT'S DICE NUMBER, AFTER CHARACTERS ARE CHOSEN"

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to read rules from a file
def read_rules(filename):
    try:
        with open(filename, 'r') as file:
            rules = [line.strip() for line in file]
        return rules
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return []

# Function to get random rules from files
def get_random_rules():
    penalties = read_rules(PENALTIES_FILE)
    advantages = read_rules(ADVANTAGES_FILE)
    return random.sample(penalties, 9), random.sample(advantages, 9)

# Function to announce rule using text-to-speech
def announce_rule(rule):
    engine.say(rule)
    print(rule)
    engine.runAndWait()

# Main function
def main():
    random_penalties, random_advantages = get_random_rules()

    while True:
        dice_roll = input("Enter your d20 roll: ")

        # Validate input
        if not dice_roll.isdigit() or not 1 <= int(dice_roll) <= 20:
            print("Error: Please enter a valid integer between 1 and 20.")
            continue

        time.sleep(1)  # Adding a 1-second delay

        dice_roll = int(dice_roll)

        # Handle the case when the dice roll is 19
        if dice_roll == 19:
            announce_rule("Roll again for forfeit.")
            continue

        # Apply rules based on dice roll
        if dice_roll == 1:
            announce_rule(YOU_SD_PENALTY)
        elif dice_roll == 20:
            announce_rule(YOU_PICK_DICE_PENALTY)
        elif dice_roll % 2 == 0:
            announce_rule(random_penalties[dice_roll // 2 - 1])
        else:
            announce_rule(random_advantages[dice_roll // 2])

        print("\n")  # Adding a line break for neatness

if __name__ == "__main__":
    main()