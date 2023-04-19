'''
import random
running = True
print("Think of any number!")
while running:
    ump = input("Press ENTER to proceed. ")
    add = random.randint(4,10)
    print("Okay, add",add,"to your number. ")
    ump = input("Press ENTER to proceed. ")
    subtract = add - 3
    print("Now, subtract",subtract,"from that number. ")
    ump = input("Press ENTER to proceed. ")
    result = int(input("What is the number you have now? "))
    print("Your original number was",result - 3,"\n\nThink of another number.")
    
'''
#AI VERSION
import random

def main():
    print("I will try to guess your number!")
    print("Please enter a number between 1 and 10")
    user_number = int(input())
    ai_number = random.randint(1,10)
    while ai_number != user_number:
        print("AI guesses: " + str(ai_number))
        print("Was I right? (y/n)")
        response = input()
        if response == "y":
            print("Yay! I win!")
            break
        else:
            ai_number = random.randint(1,10)
    print("Thanks for playing with me! You mean a lot to me!")

main()