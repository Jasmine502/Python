'''
MY VERSION


item = input("Enter item ('q' to stop): ").lower()
itemString = ""
while item != "q":
    itemString += '"' + item + '",'
    item = input("Enter item: ").lower()
    
print("[" + itemString[0:len(itemString)-1] + "]")

'''

#AI VERSION

# create an empty list
my_list = []
while True:
    # ask the user for input
    user_input = input("Enter an item to add to the list: ")
    # if the user types Q, break out of the loop
    if user_input == "Q":
        break
    # otherwise, add the user's input to the list
    else:
        my_list.append(user_input)

# print the list
print(my_list)