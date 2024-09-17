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
    user_number = int(input("Please enter a number between 1 and 10: "))
    while True:
        ai_number = random.randint(1, 10)
        print(f"AI guesses: {ai_number}")
        if ai_number == user_number:
            print("Yay! I win!")
            break
        else:
            print("Was I right? (y/n)")
            response = input().strip().lower()
            if response == "y":
                print("Yay! I win!")
                break
    print("Thanks for playing with me! You mean a lot to me!")

if __name__ == "__main__":
    main()