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

def main():
    print("Hey! I thought of a number between 1 and 10!\nCan you guess it?"
          "\nYou have 3 tries!")
    number = random.randint(1, 10)
    guess = int(input("What is your guess? "))
    count = 1
    while guess != number and count < 3:
        if guess > number:
            print("Too high!")
        else:
            print("Too low!")
        guess = int(input("What is your guess? "))
        count += 1
    if guess == number:
        print("You got it!")
    else:
        print("You lose!")
    print("The number was", number)
    again = input("Would you like to play again? (y/n) ")
    while again == "y":
        print("Hey! I thought of a number between 1 and 10!\nCan you guess it?"
              "\nYou have 3 tries!")
        number = random.randint(1, 10)
        guess = int(input("What is your guess? "))
        count = 1
        while guess != number and count < 3:
            if guess > number:
                print("Too high!")
            else:
                print("Too low!")
            guess = int(input("What is your guess? "))
            count += 1
        if guess == number:
            print("You got it!")
        else:
            print("You lose!")
        print("The number was", number)
        again = input("Would you like to play again? (y/n) ")
    print("Thanks for playing!")

main()