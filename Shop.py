class Market:
    def __init__(self):
        self.money = round(float(input("How much money do you have? £")), 2)
        self.item_quantities = {}
        self.recipes = []
        self.aisles = {
            "Produce": {"products": ["Apple", "Pear", "Orange"], "price": 0.25},
            "Dairy": {"products": ["Milk", "Cheese", "Butter", "Ice cream"], "price": 1.5},
            "Protein": {"products": ["Steak", "Pork", "Egg", "Lamb", "Ham", "Sausage", "Beef", "Chicken", "Turkey", "Fish"], "price": 2},
            "Grain": {"products": ["Sugar", "Flour", "Salt", "Rice", "Beans"], "price": 1.25},
            "Other": {"products": ["Water"], "price": 1}
        }
        self.recipe_prices = {
            "Cake": 15,
            "Chicken and Rice": 6.5,
            "Apple Crumble": 4,
            "Pear Crumble": 4,
            "Fruit Salad": 3
        }
        self.recipe_ingredients = {
            "Cake": {"Butter": 2, "Egg": 3, "Sugar": 1, "Salt": 1},
            "Chicken and Rice": {"Chicken": 2, "Rice": 3, "Salt": 1},
            "Apple Crumble": {"Flour": 1, "Salt": 1, "Butter": 1, "Water": 1, "Apple": 3},
            "Pear Crumble": {"Flour": 1, "Salt": 1, "Butter": 1, "Water": 1, "Pear": 3},
            "Fruit Salad": {"Apple": 4, "Pear": 4, "Orange": 4}
        }

    def update_money(self, amount):
        self.money = round(self.money + amount, 2)

    def main_menu(self):
        while True:
            print("\nMain Menu:")
            print("1) Enter Market")
            print("2) Make Recipes")
            print("3) Sell Recipes")
            print("4) Exit Program")
            choice = input("Choose an option: ")
            if choice == '1':
                self.enter_market()
            elif choice == '2':
                self.make_recipes()
            elif choice == '3':
                self.sell_recipes()
            elif choice == '4':
                print(f"Exiting the program. You have £{self.money:.2f} left.")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 4.")

    def enter_market(self):
        print("\nWelcome to PyMarket!")
        while True:
            print("\nAisles:\n")
            for i, aisle_name in enumerate(self.aisles, 1):
                print(f"{i}) {aisle_name}")
            print("\n6) Return to Main Menu\n")

            try:
                aisle_choice = int(input("Enter aisle: "))
                if aisle_choice == 6:
                    break
                selected_aisle = list(self.aisles.values())[aisle_choice - 1]
                self.shop_in_aisle(selected_aisle)
            except (ValueError, IndexError):
                print("Invalid choice. Please enter a number from the list.")

    def shop_in_aisle(self, aisle):
        while True:
            print()
            for i, product in enumerate(aisle['products'], 1):
                print(f"{i}. {product}")
            print(f"\n{len(aisle['products']) + 1}. Leave Aisle")

            try:
                item_choice = int(input("Enter item number: "))
                if item_choice == len(aisle['products']) + 1:
                    break
                product_name = aisle['products'][item_choice - 1]
                quantity = int(input("Enter quantity: "))
                cost = aisle['price'] * quantity

                if self.money >= cost:
                    self.update_money(-cost)
                    self.item_quantities[product_name] = self.item_quantities.get(product_name, 0) + quantity
                    print(f"\nBought {quantity} {product_name.lower()} for £{cost:.2f}")
                else:
                    print("Not enough money!")
                print(f"Money left: £{self.money:.2f}")
            except (ValueError, IndexError):
                print("Invalid choice or quantity. Please enter a valid number.")

    def make_recipes(self):
        while True:
            print("\nItems available to make recipes:")
            for item, quantity in self.item_quantities.items():
                print(f"{item}: {quantity}")
            print("\nEnter the item names to combine into a recipe (comma-separated), or 'done' to finish:")

            selected_items_input = input()
            if selected_items_input.lower() == 'done':
                break

            selected_items = selected_items_input.split(',')
            recipe_name = self.combine_items_into_recipe(selected_items)
            if recipe_name:
                self.recipes.append(recipe_name)
                print(f"Created {recipe_name}!")
            else:
                print("Those items don't make a recipe.")

    def combine_items_into_recipe(self, selected_items):
        # Convert the list of selected items to a dictionary with item counts
        selected_items_counts = {item.strip(): selected_items.count(item.strip()) for item in selected_items}
        
        # Try to find a recipe that can be made with the selected items
        for recipe_name, required_ingredients in self.recipe_ingredients.items():
            if all(self.item_quantities.get(item, 0) >= quantity for item, quantity in required_ingredients.items()):
                # If all required ingredients are available, reduce their quantities and return the recipe name
                for item, quantity in required_ingredients.items():
                    self.item_quantities[item] -= quantity
                return recipe_name
        return None

    def sell_recipes(self):
        while True:
            print("\nRecipes ready to sell:")
            for i, recipe in enumerate(self.recipes, 1):
                print(f"{i}. {recipe}")
            print("\nEnter the number of the recipe to sell, or 'done' to finish:")

            recipe_input = input()
            if recipe_input.lower() == 'done':
                break

            try:
                recipe_index = int(recipe_input) - 1
                recipe_name = self.recipes.pop(recipe_index)
                self.update_money(self.recipe_prices[recipe_name])
                print(f"Sold {recipe_name} for £{self.recipe_prices[recipe_name]}!")
            except (ValueError, IndexError):
                print("Invalid selection. Please enter a recipe number.")

# Main Program
market = Market()
market.main_menu()
