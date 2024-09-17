import os
import re
from groq import Groq

# Fetch API key from environment variables
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("API key for Groq is not set in environment variables.")
client = Groq(api_key=API_KEY)

def generate_auction_item_and_bid():
    prompt = (
        "You are an auctioneer. Provide the name of a unique auction item from pop culture (ranging from extremely commonplace to incredibly absurd), "
        "followed by a colon and its reasonable starting bid in numeric form. "
        "Respond ONLY with the item and starting bid in the format: [ITEM NAME]: [STARTING_BID]. "
        "Do NOT include any introductions, explanations, or additional text. "
        "Example: Signed Beatles Album: 10000"
    )
    conversation = [
        {"role": "system", "content": "You are an assistant that generates unique auction items with reasonable starting bids. You must follow the user's instructions precisely."},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=conversation,
        temperature=1,
        max_tokens=30,
        top_p=1,
        stream=False  # Set to False to get the entire response at once
    )

    text = response.choices[0].message.content.strip()
    try:
        item, starting_bid = text.split(':')
        formatted_bid = "{:,.2f}".format(float(starting_bid.strip()))
        return item.strip(), formatted_bid
    except ValueError:
        # In case the response format is incorrect, try again
        print(f"\nFinding new item....")
        return generate_auction_item_and_bid()

class Player:
    def __init__(self, name):
        self.name = name
        self.budget = 500000
        self.collection = []

    def bid(self, amount):
        if amount <= self.budget:
            self.budget -= amount
            return True
        return False

    def formatted_budget(self):
        return "{:,.2f}".format(self.budget)

def main():
    print("Welcome to the AI-Powered Auction Game!")
    player1_name = input("Enter name for Player 1: ")
    player2_name = input("Enter name for Player 2: ")

    player1 = Player(player1_name)
    player2 = Player(player2_name)

    while player1.budget > 0 and player2.budget > 0:
        item, starting_bid = generate_auction_item_and_bid()
        print(f"\nUp for auction: {item}")
        print(f"Starting bid: ${starting_bid}")

        bid = float(starting_bid.replace(',', ''))
        current_bid = bid
        highest_bidder = None
        pass_count = 0  # Track the number of consecutive passes
        current_player = player1
        other_player = player2

        while True:
            print(f"{current_player.name}'s turn. Budget: ${current_player.formatted_budget()}")
            player_bid = input(f"Enter your bid (or 'pass' to forfeit): ").strip().lower()

            if player_bid == 'pass':
                pass_count += 1
                if pass_count == 2:
                    if highest_bidder is None:
                        print(f"Both players passed. The item '{item}' will not be sold.")
                    else:
                        highest_bidder.collection.append(item)
                        print(f"Congratulations {highest_bidder.name}, you won the bid for {item}!")
                    break  # Exit the inner loop after two consecutive passes
                else:
                    current_player, other_player = other_player, current_player
            else:
                try:
                    player_bid = float(player_bid)
                    if player_bid > current_bid and current_player.bid(player_bid):
                        current_bid = player_bid
                        highest_bidder = current_player
                        pass_count = 0  # Reset pass count when a valid bid is made
                        current_player, other_player = other_player, current_player
                    else:
                        print("Invalid bid. Try again.")
                except ValueError:
                    print("Please enter a valid number or 'pass'.")

        # Reset players to original order for the next item
        current_player = player1
        other_player = player2

    print("\nAuction Over!")
    print("Final Collections:")
    print(f"{player1.name}: {player1.collection}, Budget left: ${player1.formatted_budget()}")
    print(f"{player2.name}: {player2.collection}, Budget left: ${player2.formatted_budget()}")

if __name__ == "__main__":
    main()
