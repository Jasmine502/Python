import random
import time

while True:
    try:
        number = int(input("What number do you want upon rolling the 6-sided die? "))
        if not 1 <= number <= 6:
            raise ValueError("The number should be between 1 and 6")
        tries = 1
        dieNo = random.randint(1, 6)
        print(f"Number rolled: {dieNo}")

        while dieNo != number:
            time.sleep(1)
            dieNo = random.randint(1, 6)
            print(f"Number rolled: {dieNo}")
            tries += 1

        print(f"It took {tries} tries to get {number}.\n")

    except ValueError as e:
        print("Invalid input:", e)
    except KeyboardInterrupt:
        print("Program terminated by user")
        break
