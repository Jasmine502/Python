import random
import time
numbers = "0123456789"
playAgain = "Y"
print ("            WELCOME TO SINGLE-PLAYER BLACKJACK")

def inputCheck(string,default):
    error = False
    for i in range(len(string)):
        if string[i] not in numbers:
            error = True
    if error == False:
        string = int(string)
    else:
        string = int(default)
    return string

while playAgain == "Y":
    deck = ["AH","2H","3H","4H","5H","6H","7H","8H","9H","TH","JH","QH","KH","AD","2D","3D","4D","5D","6D","7D","8D","9D","TD","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","TS","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","TC","JC","QC","KC"]
    hand = []
    handNo = input("\nHow many cards would you like to start with? ")
    handNo = inputCheck(handNo,"5")
    
    if (handNo < 1) or (handNo > 51):
        handNo = 5
    print ("Dealing your hand...\n")
    time.sleep(1)
    for i in range(handNo):
        card = random.randint(0,len(deck)-1)
        hand.append(deck[card])
        print("Card " + str(i+1) + ": " + str(hand[i]))
        deck.remove(deck[card])
        time.sleep(1)
    print("\nOption " + str(len(hand)+1) + ": Pick Up\nOption " + str(len(hand) + 2) + ": Sort Hand\n")
    card = random.randint(0,len(deck))
    topCard = deck[card]

    while len(hand) > 0:
        time.sleep(1)
        print ("Card on top is " + str(topCard))
        topCardRank = topCard[0]
        topCardSuit = topCard[1]
        time.sleep(0.5)
        cTP = input("Enter card/option number to place: ")
        cTP = inputCheck(cTP,str(len(hand) + 1))
        if cTP < len(hand)+1:
            cTP = hand[cTP-1]
            cTPRank = cTP[0]
            cTPSuit = cTP[1]
            print("You placed the " + str(cTP))
            time.sleep(1)

            if cTPRank == "A":
                topCardSuit = input("Change suit to ").upper()
                deck.append(topCard)
                topCard = "A" + str(topCardSuit)
                hand.remove(cTP)
                
            elif (cTPRank == topCardRank) or (cTPSuit == topCardSuit):
                deck.append(topCard)
                topCard = cTP
                hand.remove(cTP)
            else:
                print ("You pick up 2 for mistake.")
                time.sleep(1)
                for i in range(2):
                    card = random.randint(0,len(deck))
                    hand.append(deck[card])
                    deck.remove(deck[card])

        elif cTP == len(hand) + 1:
            print ("You've picked up a card.")
            time.sleep(1)
            card = random.randint(0,len(deck))
            hand.append(deck[card])
            deck.remove(deck[card])
        else:
            hand.sort()
        print()
        for i in range(len(hand)):
            print ("Card " + str(i+1) + ": " + str(hand[i]))
        if len(hand) > 0:
            time.sleep(1)
            print("\nOption " + str(len(hand)+1) + ": Pick Up\nOption " + str(len(hand) + 2) + ": Sort Hand\n")

    playAgain = input("\nCongrats!\nYou won!\n\nPlay Again? ").upper()
    
    



    





