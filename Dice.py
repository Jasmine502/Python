'''
MY VERSION

import random
import time

running = True
while running:
    number = int(input("What number do you want upon rolling the 6-sided die? "))
    tries = 0
    dieNo = random.randint(1,6)
    print ("Number rolled:",dieNo)
    tries += 1
    while dieNo != number:
        time.sleep(1)
        dieNo = random.randint(1,6)
        print ("Number rolled:",dieNo)
        tries += 1
    print ("It took",tries,"tries to get",number,"\n")

    tries = 0
'''

#AI VERSION

import random
import time

def roll_d6():
    return random.randint(1,6)

def main():
    print("Welcome to the d6 roller!")
    print("Please enter a number between 1 and 6")
    user_input = int(input())
    if user_input < 1 or user_input > 6:
        print("Please enter a number between 1 and 6")
        user_input = int(input())
    else:
        print("You entered " + str(user_input))
        print("Rolling...")
        time.sleep(1)
        roll_count = 0
        while True:
            roll_count += 1
            roll = roll_d6()
            print("You rolled a " + str(roll))
            if roll == user_input:
                print("You got your number in " + str(roll_count) + " roll(s)!")
                break
            else:
                print("Rolling again...")
                time.sleep(1)

main()