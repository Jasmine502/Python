money = float(input("How much money do you have? "))
money = round(money,2)
print ("\n     Welcome to PyMarket!")      
def moneyFormat(money):
    pounds = round(money)
    if len(str(round(money,2))) == 3 or len(str(money - pounds)) == 3:
        string = str(money) + "0"
    else:
        string = str(money)
    return string
            
items = []
produce = ["Apple","Pear","Orange"]
dairy = ["Milk","Cheese","Butter","Ice cream"]
protein = ["Steak","Pork","Egg","Lamb","Ham","Sausage","Beef","Chicken","Turkey","Fish"]
grain = ["Sugar","Flour","Salt","Rice","Beans"]
other = ["Water"]
ingredients = []
recipes = []
while 1 > 0:
    print("\n1) Enter Market\n2) Make Recipes\n3) Sell Recipes\n")
    option = int(input("Enter option number: "))
    aisle = ""
    if option == 1:
        while 1 > 0:
            print ("\nAisles:\n\n1) Produce\n2) Dairy Products\n3) Protein\n4) Grain\n5) Other\n\n6) Leave\n")
            aisle = int(input("Enter aisle: "))
            if aisle == "":
                aisle = 6
                
            if aisle == 1:
                product = produce
                price = 0.25
            elif aisle == 2:
                product = dairy
                price = 1.5
            elif aisle == 3:
                product = protein
                price = 2
            elif aisle == 4:
                product = grain
                price = 1.25
            elif aisle == 5:
                product = other
                price = 1
            elif aisle >= 6:
                break
            while 1 > 0:
                print()
                for i in range(len(product)):
                    print(str(i+1) + ". " + product[i])
                print("\n" + str(len(product) + 1) + ". Leave Aisle")

                item = int(input("Enter item number: "))
                if item == len(product) + 1:
                    break
                quantity = int(input("Enter quantity: "))
                if quantity == "":
                    quantity = 1
                cost = price * quantity


                if money >= cost:
                    for i in range(quantity):
                        money -= price
                        items.append(product[item - 1])
                    print("\nBought",quantity,product[item -1].lower() , "for £" + moneyFormat(cost))
                else:
                    print ("Not enough money!\n")
                print("Money: £" + moneyFormat(money))
    elif option == 2:
        for i in range(len(items)):
            print("Item",str(i+1) + ":", items[i])
        print("\nOption" , str(len(items) + 1) + ": Leave\n")
        option = int(input("Enter option number: "))
        while 1 > 0:
            if (option >= len(items) + 1):
                break
            else:
                ingredients.append(items[option-1])
                items.remove(items[option-1])
            for i in range(len(items)):
                print("Item",str(i+1) + ":", items[i])
            print("\nOption" , str(len(items) + 1) + ": Make\n")
            option = int(input("Enter option number: "))
            
        print ("With these ingredients:\n")
        for i in range(len(ingredients)):
            print(ingredients[i])
        print("\nYou can make:")
        while 1 > 0:
            cake = False
            chickenAndRice = False
            appleCrumble = False
            pearCrumble = False
            fruitSalad = False
                
            apple = 0
            beans = 0
            beef = 0
            butter = 0
            cheese = 0
            chicken = 0
            egg = 0
            fish = 0
            flour = 0
            ham = 0
            iceCream = 0
            lamb = 0
            milk = 0
            orange = 0
            pear = 0
            pork = 0
            rice = 0
            salt = 0
            sausage = 0
            steak = 0
            sugar = 0
            turkey = 0
            water = 0
            for i in range(len(ingredients)):
                if ingredients[i] == "Apple":
                    apple += 1                
                if ingredients[i] == "Beans":
                    beans += 1
                elif ingredients[i] == "Beef":
                    beef += 1
                elif ingredients[i] == "Butter":
                    butter += 1
                elif ingredients[i] == "Cheese":
                    cheese += 1
                elif ingredients[i] == "Chicken":
                    chicken += 1
                elif ingredients[i] == "Egg":
                    egg += 1
                elif ingredients[i] == "Fish":
                    fish += 1
                elif ingredients[i] == "Flour":
                    flour += 1
                elif ingredients[i] == "Ham":
                    ham += 1
                elif ingredients[i] == "Ice cream":
                    iceCream += 1
                elif ingredients[i] == "Lamb":
                    lamb += 1
                elif ingredients[i] == "Milk":
                    milk += 1
                elif ingredients[i] == "Orange":
                    orange += 1
                elif ingredients[i] == "Pear":
                    pear += 1
                elif ingredients[i] == "Pork":
                    pork += 1
                elif ingredients[i] == "Rice":
                    rice += 1
                elif ingredients[i] == "Salt":
                    salt += 1
                elif ingredients[i] == "Sausage":
                    sausage += 1
                elif ingredients[i] == "Steak":
                    steak += 1
                elif ingredients[i] == "Sugar":
                    sugar += 1
                elif ingredients[i] == "Turkey":
                    turkey += 1
                elif ingredients[i] == "Water":
                    water += 1
                
            if butter >= 2 and egg >= 3 and sugar >= 1 and salt >= 1:
                cake = True
                
            elif chicken >= 2 and rice >= 3 and salt >= 1:
                chickenAndRice = True

            elif flour >= 1 and salt >= 1 and butter >= 1 and water >= 1 and apple >= 3:
                appleCrumble = True

            elif flour >= 1 and salt >= 1 and butter >= 1 and water >= 1 and pear >= 3:
                pearCrumble = True
            elif apple >= 4 and pear >= 4 and orange >= 4:
                fruitSalad = True

            break
        if cake == True:
            while butter >= 2 and egg >= 3 and sugar >= 1 and salt >= 1:
                recipes.append("Cake")
                butter -= 2
                egg -= 3
                sugar -= 1
                salt -= 1
        elif chickenAndRice == True:
            while chicken >= 2 and rice >= 3 and salt >= 1:
                recipes.append("Chicken and Rice")
                chicken -= 2
                rice -= 3
                salt -= 1
        elif appleCrumble == True:
            while flour >= 1 and salt >= 1 and butter >= 1 and water >= 1 and apple >= 3:
                recipes.append("Apple Crumble")
                flour -= 1
                salt -= 1
                butter -= 1
                water -= 1
                apple -= 3
        elif pearCrumble == True:
            while flour >= 1 and salt >= 1 and butter >= 1 and water >= 1 and pear >= 3:
                recipes.append("Pear Crumble")
                flour -= 1
                salt -= 1
                butter -= 1
                water -= 1
                pear -= 3
        elif fruitSalad == True:
            while apple >= 4 and pear >= 4 and orange >= 4:
                recipes.append("Fruit Salad")
                apple -= 1
                pear -= 1
                orange -= 1
                
        else:
            print("Nothing")
        for i in range(len(recipes)):
            print(recipes[i])
    elif option == 3:
        apple = 0
        beans = 0
        beef = 0
        butter = 0
        cheese = 0
        chicken = 0
        egg = 0
        fish = 0
        flour = 0
        ham = 0
        iceCream = 0
        lamb = 0
        milk = 0
        orange = 0
        pear = 0
        pork = 0
        rice = 0
        salt = 0
        sausage = 0
        steak = 0
        sugar = 0
        turkey = 0
        water = 0
        while 1 > 0:
            price = 0
            print("Sell:\n")
            for i in range(len(recipes)):
                print(str(i+1) + ")",recipes[i])
            print("\nOption",str(len(recipes) + 1) + ": Keep Recipes")
            
            sell = int(input("Enter option number: "))

            if sell >= len(recipes) + 1:
                break
            
            elif recipes[sell - 1] == "Cake":
                money += 15
            elif recipes[sell - 1] == "Chicken and Rice":
                money += 6.5
            recipes.remove(recipes[sell - 1])
                


        
                
            
                    
                
                

        

        

        

            


    
        

        
