from random import sample
from pathlib import Path
import pyttsx3
import time

class GameRules:
    PENALTIES_FILE = Path("penalties.txt")
    ADVANTAGES_FILE = Path("advantages.txt")
    YOU_SD_PENALTY = "SEPPUKU: YOU SD 2 STOCKS"
    YOU_PICK_DICE_PENALTY = "YOU DECIDE: YOU PICK OPPONENT'S DICE NUMBER, AFTER CHARACTERS ARE CHOSEN"

    def __init__(self):
        self.engine = pyttsx3.init()

    def read_rules(self, filename):
        if not filename.exists():
            print(f"Error: {filename} not found.")
            return []

        with filename.open('r') as file:
            return [line.strip() for line in file]

    def get_random_rules(self, filename, count=9):
        rules = self.read_rules(filename)
        return sample(rules, min(len(rules), count))

    def announce_rule(self, rule):
        print(rule)
        self.engine.say(rule)
        self.engine.runAndWait()

    def validate_dice_roll(self, roll):
        return roll.isdigit() and 1 <= int(roll) <= 20

    def main(self):
        random_penalties = self.get_random_rules(self.PENALTIES_FILE)
        random_advantages = self.get_random_rules(self.ADVANTAGES_FILE)

        while True:
            dice_roll = input("Enter your d20 roll: ")

            if not self.validate_dice_roll(dice_roll):
                print("Error: Please enter a valid integer between 1 and 20.")
                continue

            time.sleep(1)  # Adding a 1-second delay
            dice_roll = int(dice_roll)

            if dice_roll == 19:
                self.announce_rule("Roll again for forfeit.")
                continue

            if dice_roll == 1:
                self.announce_rule(self.YOU_SD_PENALTY)
            elif dice_roll == 20:
                self.announce_rule(self.YOU_PICK_DICE_PENALTY)
            elif dice_roll % 2 == 0:
                self.announce_rule(random_penalties[dice_roll // 2 - 1])
            else:
                self.announce_rule(random_advantages[dice_roll // 2])

            print("\n")  # Adding a line break for neatness

if __name__ == "__main__":
    GameRules().main()
