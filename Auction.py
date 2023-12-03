import openai, re

# Initialize OpenAI GPT-3.5-turbo
openai.api_key = ''  # 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

def generate_auction_item_and_bid():
    prompt = "You are an auctioneer. Provide the name of a unique auction item (ranging from extremely commonplace to incredibly absurd), followed by a colon and its reasonable starting bid in numeric form. Format: [ITEM NAME]: [STARTING_BID]. Example: Signed Beatles Album: 10000"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=30
    )
    text = response.choices[0].text.strip()
    item, starting_bid = text.split(':')
    formatted_bid = "{:,.2f}".format(float(starting_bid.strip()))
    return item.strip(), formatted_bid

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
    current_player = player1
    other_player = player2

    while player1.budget > 0 and player2.budget > 0:
        item, starting_bid = generate_auction_item_and_bid()
        print(f"\nUp for auction: {item}")
        print(f"Starting bid: ${starting_bid}")

        bid = float(starting_bid.replace(',', ''))
        player1_bid = player2_bid = 0.0
        no_bids = True

        while True:
            print(f"{current_player.name}'s turn. Budget: ${current_player.formatted_budget()}")
            player_bid = input(f"Enter your bid (or 'pass' to forfeit): ").strip().lower()

            if player_bid == 'pass':
                if no_bids:
                    print(f"Both players passed. The item '{item}' will not be sold.")
                    break
                else:
                    winner = other_player
                    winner.collection.append(item)
                    print(f"Congratulations {winner.name}, you won the bid for {item}!")
                    break

            try:
                player_bid = float(player_bid)
                if player_bid > bid and current_player.bid(player_bid):
                    bid = player_bid
                    no_bids = False
                    if current_player == player1:
                        player1_bid = player_bid
                        current_player = player2
                        other_player = player1
                    else:
                        player2_bid = player_bid
                        current_player = player1
                        other_player = player2
                else:
                    print("Invalid bid. Try again.")
            except ValueError:
                print("Please enter a valid number or 'pass'.")

    print("\nAuction Over!")
    print("Final Collections:")
    print(f"{player1.name}: {player1.collection}, Budget left: ${player1.formatted_budget()}")
    print(f"{player2.name}: {player2.collection}, Budget left: ${player2.formatted_budget()}")

if __name__ == "__main__":
    main()

