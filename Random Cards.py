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
    #Create a list of cards
    cards = ['Ace of Spades', '2 of Spades', '3 of Spades', '4 of Spades', '5 of Spades', '6 of Spades', '7 of Spades', '8 of Spades', '9 of Spades', '10 of Spades', 'Jack of Spades', 'Queen of Spades', 'King of Spades',
             'Ace of Hearts', '2 of Hearts', '3 of Hearts', '4 of Hearts', '5 of Hearts', '6 of Hearts', '7 of Hearts', '8 of Hearts', '9 of Hearts', '10 of Hearts', 'Jack of Hearts', 'Queen of Hearts', 'King of Hearts',
             'Ace of Clubs', '2 of Clubs', '3 of Clubs', '4 of Clubs', '5 of Clubs', '6 of Clubs', '7 of Clubs', '8 of Clubs', '9 of Clubs', '10 of Clubs', 'Jack of Clubs', 'Queen of Clubs', 'King of Clubs',
             'Ace of Diamonds', '2 of Diamonds', '3 of Diamonds', '4 of Diamonds', '5 of Diamonds', '6 of Diamonds', '7 of Diamonds', '8 of Diamonds', '9 of Diamonds', '10 of Diamonds', 'Jack of Diamonds', 'Queen of Diamonds', 'King of Diamonds']
    #Create a list of the users hand
    hand = []
    #Ask the user how many cards they want
    numCards = int(input('How many cards would you like? '))
    #Validate the input
    while numCards < 1 or numCards > 52:
        print('Invalid input. Please enter a number between 1 and 52.')
        numCards = int(input('How many cards would you like? '))
    #Pick the cards
    for i in range(numCards):
        card = random.choice(cards)
        hand.append(card)
        cards.remove(card)
    #Print the users hand
    for i in range(numCards):
        print(hand[i])
while True:
    main()