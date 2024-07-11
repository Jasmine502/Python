import os

class Character:
    def __init__(self, name, race, char_class, level, age, strength, dexterity, constitution, intelligence, wisdom, charisma, base_hp, base_ac, equipment, xp, gold):
        self.name = name
        self.race = race
        self.char_class = char_class
        self.level = level
        self.age = age
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.base_hp = base_hp
        self.current_hp = base_hp
        self.base_ac = base_ac
        self.equipment = equipment
        self.xp = xp
        self.gold = gold
        self.armor_bonus = 0

    def calculate_modifier(self, score):
        return (score // 2) - 5

    def calculate_ac(self):
        return 10 + self.calculate_modifier(self.dexterity) + self.armor_bonus

    def calculate_passive_perception(self):
        return 10 + self.calculate_modifier(self.wisdom)

    def format_modifier(self, modifier):
        return f"+{modifier}" if modifier >= 0 else f"{modifier}"

    def calculate_proficiency_bonus(self):
        # +2 for Lv 1-4, +3 for Lv 5-8,
        # +4 for Lv 9-12, +5 for Lv 13-16, +6 for Lv 17-20
        if self.level <= 4:
            return 2
        elif self.level <= 8:
            return 3
        elif self.level <= 12:
            return 4
        elif self.level <= 16:
            return 5
        else:
            return 6
        
    def display_info(self):
        info = (
            "====================================================\n"
            f"Name: {self.name}\n"
            f"Race: {self.race}\n"
            f"Class: {self.char_class}\n"
            f"Level: {self.level}\n"
            f"Proficiency Bonus: +{self.calculate_proficiency_bonus()}\n"
            f"Age: {self.age}\n"
            "Ability Scores:\n"
            "----------------\n"
            f"STR: {self.strength} ({self.format_modifier(self.calculate_modifier(self.strength))})\n"
            f"DEX: {self.dexterity} ({self.format_modifier(self.calculate_modifier(self.dexterity))})\n"
            f"CON: {self.constitution} ({self.format_modifier(self.calculate_modifier(self.constitution))})\n"
            f"INT: {self.intelligence} ({self.format_modifier(self.calculate_modifier(self.intelligence))})\n"
            f"WIS: {self.wisdom} ({self.format_modifier(self.calculate_modifier(self.wisdom))})\n"
            f"CHA: {self.charisma} ({self.format_modifier(self.calculate_modifier(self.charisma))})\n"
            f"Hit Points: {self.current_hp}/{self.base_hp}\n"
            f"Armor Class: {self.calculate_ac()}\n"
            f"Passive Perception: {self.calculate_passive_perception()}\n"
            "----------------\n"
            f"Equipment: {', '.join(self.equipment)}\n"
            f"Gold: {self.gold} gp\n"
            f"Current XP: {self.xp}\n"

        )
        print(info)

    def update_hp(self, amount):
        self.current_hp = max(0, min(self.current_hp + amount, self.base_hp))
        print(f"HP updated to: {self.current_hp}/{self.base_hp}")

    def update_xp(self, amount):
        self.xp += amount
        print(f"XP updated to: {self.xp}")

    def add_equipment(self, item):
        self.equipment.append(item)
        print(f"Equipment updated: {', '.join(self.equipment)}")

    def remove_equipment(self, item):
        if item in self.equipment:
            self.equipment.remove(item)
            print(f"Equipment updated: {', '.join(self.equipment)}")
        else:
            print(f"Item '{item}' not found in equipment.")

    def update_gold(self, amount):
        if self.gold + amount >= 0:
            self.gold += amount
            print(f"Gold updated to: {self.gold} gp")
        else:
            print("Cannot have negative gold.")

    def set_armor_bonus(self, bonus):
        self.armor_bonus = bonus
        print(f"Armor bonus set to: {self.armor_bonus}")

    def save_to_file(self, filename='character_sheet.txt'):
        with open(filename, 'w') as file:
            file.write(
                f"{self.name}\n"
                f"{self.race}\n"
                f"{self.char_class}\n"
                f"{self.level}\n"
                f"{self.age}\n"
                f"{self.strength}\n"
                f"{self.dexterity}\n"
                f"{self.constitution}\n"
                f"{self.intelligence}\n"
                f"{self.wisdom}\n"
                f"{self.charisma}\n"
                f"{self.base_hp}\n"
                f"{self.base_ac}\n"
                f"{', '.join(self.equipment)}\n"
                f"{self.xp}\n"
                f"{self.gold}\n"
            )
        print(f"Character sheet saved to {filename}")

    @staticmethod
    def load_from_file(filename='character_sheet.txt'):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                lines = [line.strip() for line in file.readlines()]
                return Character(
                    name=lines[0],
                    race=lines[1],
                    char_class=lines[2],
                    level=int(lines[3]),
                    age=int(lines[4]),
                    strength=int(lines[5]),
                    dexterity=int(lines[6]),
                    constitution=int(lines[7]),
                    intelligence=int(lines[8]),
                    wisdom=int(lines[9]),
                    charisma=int(lines[10]),
                    base_hp=int(lines[11]),
                    base_ac=int(lines[12]),
                    equipment=lines[13].split(', '),
                    xp=int(lines[14]),
                    gold=int(lines[15])
                )
        else:
            print("No saved character sheet found. Using default character.")
            return None



def main():
    character = Character.load_from_file() or Character(
        name="Jazzers", race="Half-Orc", char_class="Fighter", level=1, age=24,
        strength=16, dexterity=12, constitution=14, intelligence=10, wisdom=10, charisma=8,
        base_hp=12, base_ac=11, equipment=["Double-ended Warhammer", "Tube of acid for coating", "Golden pickle trinket"], xp=50, gold=15
    )

    while True:
        print("\nMain Menu:")
        print("1. View character information")
        print("2. Update values")
        print("3. Manage equipment")
        print("4. Save character sheet to file")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            character.display_info()
        elif choice == '2':
            while True:
                print("\nUpdate Values Menu:")
                print("1. Update HP")
                print("2. Update XP")
                print("3. Update gold")
                print("4. Set armor bonus")
                print("5. Return to main menu")

                sub_choice = input("Enter your choice: ")

                if sub_choice == '1':
                    print(f"Current HP: {character.current_hp}/{character.base_hp}")
                    amount = int(input("Enter HP change: "))
                    character.update_hp(amount)
                elif sub_choice == '2':
                    print(f"Current XP: {character.xp}")
                    amount = int(input("Enter XP change: "))
                    character.update_xp(amount)
                elif sub_choice == '3':
                    print(f"Current gold: {character.gold} gp")
                    amount = int(input("Enter gold change: "))
                    character.update_gold(amount)
                elif sub_choice == '4':
                    print(f"Current armor bonus: {character.armor_bonus}")
                    bonus = int(input("Enter armor bonus: "))
                    character.set_armor_bonus(bonus)
                elif sub_choice == '5':
                    break
                else:
                    print("Invalid choice.")
        elif choice == '3':
            while True:
                print("\nManage Equipment Menu:")
                print("1. Add equipment")
                print("2. Remove equipment")
                print("3. Return to main menu")

                sub_choice = input("Enter your choice: ")

                if sub_choice == '1':
                    item = input("Enter item to add: ")
                    character.add_equipment(item)
                elif sub_choice == '2':
                    print(f"Current equipment: {', '.join(character.equipment)}")
                    item = input("Enter item to remove: ")
                    if item in character.equipment:
                        character.remove_equipment(item)
                    else:
                        print("Item not found in equipment.")
                elif sub_choice == '3':
                    break
                else:
                    print("Invalid choice.")
        elif choice == '4':
            character.save_to_file()
            print("Character sheet saved to file.")
        elif choice == '5':
            character.save_to_file()
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
