from random import sample
from pathlib import Path
import pyttsx3
import time

class GameRules:
    PENALTIES_FILE = Path("D20 Smash/penalties.txt")
    ADVANTAGES_FILE = Path("D20 Smash/advantages.txt")
    SPECIAL_RULES = {
        1: "SEPPUKU: YOU SD 2 STOCKS",
        19: "Roll again for forfeit.",
        20: "YOU DECIDE: YOU PICK OPPONENT'S DICE NUMBER, AFTER CHARACTERS ARE CHOSEN"
    }

    def __init__(self):
        self.engine = pyttsx3.init()
        self.penalties = self.read_rules(self.PENALTIES_FILE)
        self.advantages = self.read_rules(self.ADVANTAGES_FILE)

    def read_rules(self, filename):
        try:
            with filename.open('r') as file:
                return [line.strip() for line in file]
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
            return []

    def get_random_rules(self, rules, count=9):
        return sample(rules, min(len(rules), count))

    def announce_rule(self, rule):
        print(rule)
        self.engine.say(rule)
        self.engine.runAndWait()

    def get_rule(self, dice_roll):
        if dice_roll in self.SPECIAL_RULES:
            return self.SPECIAL_RULES[dice_roll]
        elif dice_roll % 2 == 0:
            return self.penalties[dice_roll // 2 - 1]
        else:
            return self.advantages[dice_roll // 2]

    def main(self):
        while True:
            try:
                dice_roll = int(input("Enter your d20 roll: "))
                if not 1 <= dice_roll <= 20:
                    raise ValueError
            except ValueError:
                print("Error: Please enter a valid integer between 1 and 20.")
                continue

            time.sleep(1)
            rule = self.get_rule(dice_roll)
            self.announce_rule(rule)

            if dice_roll == 19:
                continue

            print("\n")

if __name__ == "__main__":
    GameRules().main()
