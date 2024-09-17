'''
import random
while 1 > 0:
    cards = ["AH","2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH", "AD","2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD", "AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS", "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC"]
    handNo = int(input("How many cards would you like? "))
    if handNo < 1:
        handNo = 1
    elif handNo > 52:
        handNo = 52
        
    hand = []
    for i in range(handNo):
        card = random.randint(0,51)
        while cards[card] in hand:
            card = random.randint(0,51)
        hand.append(cards[card])
    print ("Your Hand:")
    for i in range(len(hand)):
        print("  ",hand[i])
    print()
    
'''

import random

def main():
    # Create a list of cards
    suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
    ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    cards = [f'{rank} of {suit}' for suit in suits for rank in ranks]

    # Ask the user how many cards they want
    while True:
        try:
            num_cards = int(input('How many cards would you like? '))
            if 1 <= num_cards <= 52:
                break
            else:
                print('Invalid input. Please enter a number between 1 and 52.')
        except ValueError:
            print('Invalid input. Please enter a valid number.')

    # Pick the cards
    hand = random.sample(cards, num_cards)

    # Print the user's hand
    print("Your Hand:")
    for card in hand:
        print(card)

if __name__ == "__main__":
    while True:
        main()