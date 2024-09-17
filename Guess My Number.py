'''
import random
running = True
print ("I thought of a number between 1 and 10...\nTry and guess what it is!")
while running:
    number = random.randint(1,10)
    guess = int(input("Guess: "))

    while guess != number:
        guess = int(input("Wrong!\nTry again: "))
    print ("Well done! It was",number)
    print ("\nI thought of another number, guess that!")
    
'''

#AI VERSION

import random

def get_user_guess():
    while True:
        try:
            return int(input("What's your guess, darling? "))
        except ValueError:
            print("That's not a number I recognize... Try again.")

def play_game():
    number = random.randint(1, 10)
    print("I've got a number between 1 and 10 in mind.\nYou've got three shots to guess it.")
    for count in range(1, 4):
        guess = get_user_guess()
        if guess == number:
            print("Impressive... You've got it!")
            return True
        elif guess > number:
            print("Too high, try to lower your sights.")
        else:
            print("Too low, aim a bit higher.")
        print(f"Attempt {count}/3")
    print(f"Oh, out of tries. It was {number}.")
    return False

def main():
    print("Hey there, ready to play a guessing game?")
    while input("Feeling lucky? Want to go again? (y/n) ").lower() == 'y':
        play_game()
    print("Thanks for playing with me. Ta-ta!")

if __name__ == "__main__":
    main()
