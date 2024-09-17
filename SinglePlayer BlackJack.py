import random
import time

numbers = "0123456789"
suits = ["H", "D", "S", "C"]
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]

def create_deck():
    return [rank + suit for suit in suits for rank in ranks]

def input_check(string, default):
    return int(string) if string.isdigit() else int(default)

print("            WELCOME TO SINGLE-PLAYER BLACKJACK")

while True:
    deck = create_deck()
    hand = []
    hand_no = input("\nHow many cards would you like to start with? ")
    hand_no = input_check(hand_no, "5")
    hand_no = min(max(hand_no, 1), 51)

    print("Dealing your hand...\n")
    time.sleep(1)

    for i in range(hand_no):
        card = random.choice(deck)
        hand.append(card)
        deck.remove(card)
        print(f"Card {i+1}: {card}")
        time.sleep(1)

    print(f"\nOption {len(hand)+1}: Pick Up\nOption {len(hand)+2}: Sort Hand\n")
    top_card = random.choice(deck)

    while hand:
        print(f"Card on top is {top_card}")
        top_card_rank, top_card_suit = top_card[0], top_card[1]
        ctp = input("Enter card/option number to place: ")
        ctp = input_check(ctp, str(len(hand) + 1))

        if ctp < len(hand) + 1:
            ctp = hand[ctp-1]
            ctp_rank, ctp_suit = ctp[0], ctp[1]
            print(f"You placed the {ctp}")

            if ctp_rank == "A":
                top_card_suit = input("Change suit to ").upper()
                deck.append(top_card)
                top_card = f"A{top_card_suit}"
                hand.remove(ctp)

            elif ctp_rank == top_card_rank or ctp_suit == top_card_suit:
                deck.append(top_card)
                top_card = ctp
                hand.remove(ctp)

            else:
                print("You pick up 2 for mistake.")
                for _ in range(2):
                    card = random.choice(deck)
                    hand.append(card)
                    deck.remove(card)

        elif ctp == len(hand) + 1:
            print("You've picked up a card.")
            card = random.choice(deck)
            hand.append(card)
            deck.remove(card)

        else:
            hand.sort()

        print()
        for i, card in enumerate(hand):
            print(f"Card {i+1}: {card}")

        if hand:
            print(f"\nOption {len(hand)+1}: Pick Up\nOption {len(hand)+2}: Sort Hand\n")

    play_again = input("\nCongrats!\nYou won!\n\nPlay Again? ").upper()
    if play_again != "Y":
        break