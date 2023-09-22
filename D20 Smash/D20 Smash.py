import random
import pyttsx3
import time

# Function to read rules from a file
def read_rules(filename):
    try:
        with open(filename, 'r') as file:
            rules = [line.strip() for line in file.readlines()]
        return rules
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return []

# List of penalties and advantages
penalties = read_rules("penalties.txt")
advantages = read_rules("advantages.txt")

# Pre-determined penalties
you_sd_penalty = "SEPPUKU: YOU SD 2 STOCKS"
you_pick_dice_penalty = "YOU DECIDE: YOU PICK OPPONENT'S DICE NUMBER, AFTER CHARACTERS ARE CHOSEN"

# Initialize text-to-speech engine
engine = pyttsx3.init()

def get_random_rules():
    random_penalties = random.sample(penalties, 9)
    random_advantages = random.sample(advantages, 9)
    return random_penalties, random_advantages

def announce_rule(rule):
    engine.say(rule)
    print(f"{rule}")
    engine.runAndWait()

def main():
    random_penalties, random_advantages = get_random_rules()

    while True:
        try:
            dice_roll = int(input("Enter your d20 roll: "))
        except ValueError:
            print("Error: Please enter a valid integer.")
            continue

        time.sleep(1)  # Adding a 1-second delay

        if dice_roll == 1:
            announce_rule(you_sd_penalty)
        elif dice_roll == 20:
            announce_rule(you_pick_dice_penalty)
        elif dice_roll % 2 == 0 and 0 < dice_roll // 2 - 1 < len(random_penalties):
            announce_rule(random_penalties[dice_roll // 2 - 1])
        elif 0 < dice_roll // 2 < len(random_advantages):
            announce_rule(random_advantages[dice_roll // 2 - 1])
        else:
            print("Error: Invalid d20 roll. Please enter a number between 1 and 20.")

        print("\n")  # Adding a line break for neatness

if __name__ == "__main__":
    main()
