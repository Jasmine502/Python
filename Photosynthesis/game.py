import random
import time
import pygame  # Import pygame for sound effects

# Initialize Pygame for sound
pygame.mixer.init()

# --- Game Data ---

PLAYER_NAME = "Grumblesprout"  # Default name, can be customized later
PLAYER_HEALTH = 100
PLAYER_ATTACK = 10
PLAYER_SUNLIGHT = 0  # For permanent upgrades

LEVEL = 1
LEVEL_REACHED = 1 #for tracking highest level reached

MAP_WIDTH = 25
MAP_HEIGHT = 10

BLOOMSTONE_CHANCE = 0.15  # Chance of a bloomstone appearing in a tile
MAGMAFACE_CHANCE = 0.10 # Chance of a magmaface spawning
UPGRADE_COST_INCREMENT = 25

#upgrade costs
HEALTH_UPGRADE_COST = 50
ATTACK_UPGRADE_COST = 75

#Upgrade levels
HEALTH_UPGRADE_LEVEL = 0
ATTACK_UPGRADE_LEVEL = 0

# Enemy Data
MAGMAFACE_BASE_HEALTH = 30
MAGMAFACE_BASE_ATTACK = 5
MAGMAFACE_TYPES = ["Embergrunt", "Ash Spitter", "Lava Strider", "Boulder Brother"]

# --- Functions ---

def clear_screen():
    """Clears the console screen."""
    print("\033[H\033[J", end="")  # ANSI escape code for clearing

def display_map(player_x, player_y, bloomstone_locations, magmaface_locations, boost_location):
    """Displays the game map with player, bloomstones, and enemies."""
    map_display = ""
    for y in range(MAP_HEIGHT):
        row = ""
        for x in range(MAP_WIDTH):
            if x == player_x and y == player_y:
                row += "G"  # Grumblesprout
            elif (x, y) in bloomstone_locations:
                row += "D" # bloomstone (diamond)
            elif (x,y) == boost_location:
                row += "B" # boost
            elif (x, y) in magmaface_locations:
                row += "M"  # Magmaface
            else:
                row += "." # Empty Tile
        map_display += row + "\n"

    print(map_display)
    print("G: Grumblesprout, D: Bloomstone, M: Magmaface, B: Boost, .: Empty")
    print(f"Level: {LEVEL}")

def display_status(health, attack, sunlight):
    """Displays player's health, attack, and sunlight."""
    print(f"Health: {health}")
    print(f"Attack: {attack}")
    print(f"Sunlight: {sunlight}")

def generate_level(level):
  """Generates the level data - bloomstones, boost and magmaface locations."""
  bloomstone_locations = set()
  magmaface_locations = set()
  boost_location = None

  for y in range(MAP_HEIGHT):
      for x in range(MAP_WIDTH):
          if random.random() < BLOOMSTONE_CHANCE:
              bloomstone_locations.add((x, y))
          if random.random() < MAGMAFACE_CHANCE:
              magmaface_locations.add((x, y))
  boost_location = (random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1))
  return bloomstone_locations, magmaface_locations, boost_location

def move_player(player_x, player_y, direction):
    """Moves the player in the specified direction."""
    new_x, new_y = player_x, player_y
    if direction == "w":
        new_y -= 1
    elif direction == "s":
        new_y += 1
    elif direction == "a":
        new_x -= 1
    elif direction == "d":
        new_x += 1

    # Keep player within map bounds
    new_x = max(0, min(new_x, MAP_WIDTH - 1))
    new_y = max(0, min(new_y, MAP_HEIGHT - 1))

    return new_x, new_y

def play_sound(sound_file):
    """Plays a sound effect."""
    pygame.mixer.Sound(sound_file).play()

def generate_enemy_stats(level):
    """Generates randomized enemy stats based on the current level."""
    health = MAGMAFACE_BASE_HEALTH + (level * 5)  # Scale health with level
    attack = MAGMAFACE_BASE_ATTACK + (level * 2)  # Scale attack with level
    return health, attack

def move_enemies(magmaface_locations):
    """Randomly moves enemies around the map."""
    for (x, y) in list(magmaface_locations):
        direction = random.choice(["w", "a", "s", "d"])
        new_x, new_y = x, y
        if direction == "w":
            new_y -= 1
        elif direction == "s":
            new_y += 1
        elif direction == "a":
            new_x -= 1
        elif direction == "d":
            new_x += 1

        # Keep enemy within map bounds
        new_x = max(0, min(new_x, MAP_WIDTH - 1))
        new_y = max(0, min(new_y, MAP_HEIGHT - 1))

        # Update enemy location
        magmaface_locations.remove((x, y))
        magmaface_locations.add((new_x, new_y))

def handle_combat(player_health, player_attack, magmaface_locations, player_x, player_y, sunlight):
    """Handles combat encounters."""
    if (player_x, player_y) in magmaface_locations:
        print("\nA Magmaface appears!")
        magmaface_health, magmaface_attack = generate_enemy_stats(LEVEL)
        while player_health > 0 and magmaface_health > 0:
            action = input("Fight (f) or Run (r)? ")
            if action.lower() == "f":
                magmaface_health -= player_attack
                print(f"You headbutt the Magmaface! It takes {player_attack} damage.")
                if magmaface_health <= 0:
                    print("You defeated the Magmaface!")
                    sunlight += 10 # small sunlight reward
                    magmaface_locations.remove((player_x, player_y))
                    break
                else:
                    player_health -= magmaface_attack
                    print(f"The Magmaface attacks! You take {magmaface_attack} damage.")

            elif action.lower() == "r":
                #Simple chance of success
                if random.random() < 0.5:
                    print("You manage to escape!")
                    return player_health, sunlight
                else:
                    player_health -= magmaface_attack
                    print(f"You fail to escape! The Magmaface attacks! You take {magmaface_attack} damage.")
            else:
                print("Invalid action.")
                continue

            if player_health <= 0:
                print("You have been defeated...")
                break

        return player_health, sunlight
    else:
        return player_health, sunlight

def handle_bloomstone(player_x, player_y, bloomstone_locations, attack):
    """Handles collecting bloomstones."""
    if (player_x, player_y) in bloomstone_locations:
        print("\n*Crystalline Chime!* You found a Bloomstone!")
        play_sound("collect.ogg")  # Play sound effect
        attack += 5  # Temporary boost
        bloomstone_locations.remove((player_x, player_y))
        print("+5 attack (temporary)")
        return attack
    return attack

def handle_boost(player_x, player_y, boost_location, attack):
    """Handles collecting the boost diamond"""
    if (player_x, player_y) == boost_location:
        print("\n*Whoosh wub!* You found a Boost Diamond!")
        attack += 15 # temporary boost
        print("+15 attack (temporary)")
        return attack
    return attack

def handle_level_end(player_x, player_y):
    """Handles level progression."""
    if player_x == MAP_WIDTH - 1:
        print("\nYou found the exit! Preparing for the next level...")
        time.sleep(1)  # Pause for dramatic effect
        return True
    return False

def upgrade_menu(sunlight, health, attack):
    """Handles the upgrade menu."""
    global HEALTH_UPGRADE_LEVEL, ATTACK_UPGRADE_LEVEL, HEALTH_UPGRADE_COST, ATTACK_UPGRADE_COST
    while True:
        print("\n--- Upgrade Menu ---")
        print(f"Sunlight: {sunlight}")
        print(f"1. Increase Max Health (+20, Currently +{20*HEALTH_UPGRADE_LEVEL}) - Cost: {HEALTH_UPGRADE_COST} Sunlight")
        print(f"2. Increase Base Attack (+3, Currently +{3*ATTACK_UPGRADE_LEVEL}) - Cost: {ATTACK_UPGRADE_COST} Sunlight")
        print("3. Exit")

        choice = input("Choose an upgrade (1-3): ")

        if choice == "1":
            if sunlight >= HEALTH_UPGRADE_COST:
                sunlight -= HEALTH_UPGRADE_COST
                HEALTH_UPGRADE_LEVEL += 1
                HEALTH_UPGRADE_COST += UPGRADE_COST_INCREMENT
                health += 20
                play_sound("boost.ogg")  # Play sound effect
                print("Health upgraded!")
            else:
                print("Not enough sunlight.")

        elif choice == "2":
            if sunlight >= ATTACK_UPGRADE_COST:
                sunlight -= ATTACK_UPGRADE_COST
                ATTACK_UPGRADE_LEVEL += 1
                ATTACK_UPGRADE_COST += UPGRADE_COST_INCREMENT
                attack += 3
                play_sound("boost.ogg")  # Play sound effect
                print("Attack upgraded!")
            else:
                print("Not enough sunlight.")

        elif choice == "3":
            break
        else:
            print("Invalid choice.")
    return sunlight, health, attack

def game_over(level, player_sunlight, level_reached):
    """Handles the game over sequence."""
    print("\n--- Game Over ---")
    print(f"You reached level {level}.")
    print(f"Highest Level Reached: {level_reached}")
    print(f"Sunlight earned: {player_sunlight}")
    print("Grumblesprout's rage fades...")

def game_win():
  """Handles the game win sequence."""
  print("\n--- Congratulation! ---")
  print("You have defeated the pyroclastic prime and cleansed the volcanic lands!")
  print("The Green Glade starts to grow again")

# --- Game Loop ---
def main():
    """Main game loop."""
    global LEVEL, PLAYER_HEALTH, PLAYER_ATTACK, PLAYER_SUNLIGHT, LEVEL_REACHED

    #Intro
    clear_screen()
    print("Photosynthesis: The Revenge of Verdant Fury")
    print("Awaken the Grumblesprout to avenge the destruction of The Green Glade!")
    input("Press Enter to start...")
    clear_screen()

    player_x = 0
    player_y = MAP_HEIGHT // 2  # Start in the middle of the left edge
    health = PLAYER_HEALTH + (20 * HEALTH_UPGRADE_LEVEL)
    attack = PLAYER_ATTACK + (3 * ATTACK_UPGRADE_LEVEL)
    sunlight = PLAYER_SUNLIGHT

    bloomstone_locations, magmaface_locations, boost_location = generate_level(LEVEL)

    turn_counter = 0  # Initialize turn counter

    while health > 0:
        clear_screen()
        display_map(player_x, player_y, bloomstone_locations, magmaface_locations, boost_location)
        display_status(health, attack, sunlight)

        # Move enemies every 2 turns
        if turn_counter % 2 == 0:
            move_enemies(magmaface_locations)  # Move enemies every 2 turns

        action = input("Move (WASD), Upgrade (u), or Quit (q): ").lower()

        if action in ["w", "a", "s", "d"]:
            player_x, player_y = move_player(player_x, player_y, action)
            attack = handle_bloomstone(player_x, player_y, bloomstone_locations, attack)  # Check for temporary powerup on pickup
            attack = handle_boost(player_x, player_y, boost_location, attack)  # Check for temporary powerup on pickup
            health, sunlight = handle_combat(health, attack, magmaface_locations, player_x, player_y, sunlight)  # Check for enemies
            if handle_level_end(player_x, player_y):
                LEVEL += 1
                if LEVEL > LEVEL_REACHED:
                    LEVEL_REACHED = LEVEL
                # Prepare for next level
                player_x = 0  # Start player on the left
                bloomstone_locations, magmaface_locations, boost_location = generate_level(LEVEL)
                # Reset attack to base damage
                attack = PLAYER_ATTACK + (3 * ATTACK_UPGRADE_LEVEL)

        elif action == "u":
            sunlight, health, attack = upgrade_menu(sunlight, health, attack)
        elif action == "q":
            print("Quitting game.")
            break
        else:
            print("Invalid action.")

        turn_counter += 1  # Increment turn counter

    # after the loop ends, check game over or win
    if health <= 0:
      game_over(LEVEL, sunlight, LEVEL_REACHED)
    else:
      game_win()

# --- Start the Game ---
if __name__ == "__main__":
    main()