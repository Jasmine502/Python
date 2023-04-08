import random
import time

numbers = "0123456789"
suits = ["H", "D", "S", "C"]
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
deck = []

for suit in suits:
    for rank in ranks:
        card = rank + suit
        deck.append(card)

print("            WELCOME TO SINGLE-PLAYER BLACKJACK")

def inputCheck(string, default):
    if all(char in numbers for char in string):
        return int(string)
    else:
        return int(default)

while True:
    hand = []
    handNo = input("\nHow many cards would you like to start with? ")
    handNo = inputCheck(handNo, "5")
    handNo = min(max(handNo, 1), 51)

    print("Dealing your hand...\n")
    time.sleep(1)

    for i in range(handNo):
        card = random.choice(deck)
        hand.append(card)
        deck.remove(card)
        print(f"Card {i+1}: {card}")
        time.sleep(1)

    print(f"\nOption {len(hand)+1}: Pick Up\nOption {len(hand)+2}: Sort Hand\n")
    topCard = random.choice(deck)

    while hand:
        time.sleep(1)
        print(f"Card on top is {topCard}")
        topCardRank, topCardSuit = topCard[0], topCard[1]
        cTP = input("Enter card/option number to place: ")
        cTP = inputCheck(cTP, str(len(hand) + 1))

        if cTP < len(hand) + 1:
            cTP = hand[cTP-1]
            cTPRank, cTPSuit = cTP[0], cTP[1]
            print(f"You placed the {cTP}")
            time.sleep(1)

            if cTPRank == "A":
                topCardSuit = input("Change suit to ").upper()
                deck.append(topCard)
                topCard = f"A{topCardSuit}"
                hand.remove(cTP)

            elif cTPRank == topCardRank or cTPSuit == topCardSuit:
                deck.append(topCard)
                topCard = cTP
                hand.remove(cTP)

            else:
                print("You pick up 2 for mistake.")
                time.sleep(1)

                for i in range(2):
                    card = random.choice(deck)
                    hand.append(card)
                    deck.remove(card)

        elif cTP == len(hand) + 1:
            print("You've picked up a card.")
            time.sleep(1)
            card = random.choice(deck)
            hand.append(card)
            deck.remove(card)

        else:
            hand.sort()

        print()
        for i, card in enumerate(hand):
            print(f"Card {i+1}: {card}")

        if hand:
            time.sleep(1)
            print(f"\nOption {len(hand)+1}: Pick Up\nOption {len(hand)+2}: Sort Hand\n")

    playAgain = input("\nCongrats!\nYou won!\n\nPlay Again? ").upper()
    if playAgain != "Y":
        break