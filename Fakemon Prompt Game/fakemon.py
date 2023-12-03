import random
import os
import sys
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_input_for_category(category, description):
    print(f"Choose a value for {category}. {description}")
    return input("Enter your value: ")

def get_participant_names():
    participants = []
    while (name := input("Enter participant name (or press Enter to finish): ").strip()):
        participants.append(name)
    return participants

def main():
    try:
        categories = {
            "Environment": "An environment is the natural world in which the Fakemon lives.",
            "Personality": "Personality refers to the character traits and behaviors of the Fakemon.",
            "Height": "Height is the physical stature of the Fakemon.",
            "Type": "Type refers to the Pokémon types like Fire, Water, etc. Choose one primary type.",
            "Secondary Type": "Choose one secondary type for your Fakemon, different from the primary type.",
            "Color Palette 1": "Choose the first two colors of the Fakemon's appearance.",
            "Color Palette 2": "Choose the second set of two colors for the Fakemon's appearance.",
            "Power": "Power is a unique ability or strength that the Fakemon possesses.",
            "Ability": "Ability refers to a special skill or capability that the Fakemon has.",
            "Body Shape": "Body Shape describes the physical form or structure of the Fakemon.",
            "HP": "HP is a measure of the Fakemon's health. Choose a value between 1 and 255.",
            "ATK": "ATK is the measure of the Fakemon's physical power. Choose a value between 5 and 190.",
            "DEF": "DEF is the measure of the Fakemon's resistance to physical attacks. Choose a value between 5 and 230.",
            "SpA": "SpA is the measure of the Fakemon's power in special attacks. Choose a value between 10 and 194.",
            "SpD": "SpD is the measure of the Fakemon's resistance to special attacks. Choose a value between 20 and 230.",
            "Spe": "Spe is the measure of how fast the Fakemon can move. Choose a value between 5 and 180."
        }

        participants = get_participant_names()
        if not participants:
            print("No participants entered. Exiting program.")
            sys.exit()

        primary_categories = ["Environment", "Personality", "Height", "Power", "Ability", "Body Shape"]
        stat_categories = ["HP", "ATK", "DEF", "SpA", "SpD", "Spe"]
        random.shuffle(primary_categories)
        random.shuffle(stat_categories)

        category_list = primary_categories + stat_categories + ["Type", "Secondary Type", "Color Palette 1", "Color Palette 2"]
        random.shuffle(category_list)

        responses = {}
        for i, category in enumerate(category_list):
            player = participants[i % len(participants)]
            print(f"{player}, it's your turn.")
            responses[category] = get_input_for_category(category, categories[category])
            clear_screen()
            next_player = participants[(i + 1) % len(participants)]
            print(f"Next up: {next_player}")
            time.sleep(1.5)
            clear_screen()


        final_text = "As a Fakemon designer, your task is to create a unique and enthralling Fakemon based on the provided categories.\n\n"

        for category in category_list:
            final_text += f"{category}: {responses.get(category, 'N/A')}\n"

        with open('fakemon_responses.txt', 'w') as file:
            file.write(final_text)

        print("Fakemon creation is complete! Responses saved to fakemon_responses.txt.")
        time.sleep(2)
        clear_screen()

    except KeyboardInterrupt:
        print("\nProgram interrupted.")
        sys.exit()

if __name__ == "__main__":
    main()