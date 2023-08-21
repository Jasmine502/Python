import pyperclip

# Read data from a text file
def read_data(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

# Create a dictionary from the data
def create_uuid_data(data):
    uuid_data = {}
    lines = data.split('\n')
    for line in lines:
        line = line.strip()
        if line:
            parts = line.rsplit(' (', 1)
            if len(parts) == 2:
                uuid = parts[0]
                in_game_name = parts[1][:-1]  # Remove closing parenthesis
                uuid_data[in_game_name] = uuid
    return uuid_data

# Function to search and retrieve UUIDs
def search_uuids(uuid_data, search_term):
    matching_uuids = []
    for name, uuid in uuid_data.items():
        if search_term.lower() in name.lower():
            matching_uuids.append((name, uuid))
    return matching_uuids

# User input for selecting a result
def select_result(results):
    print("Matching results:")
    for i, (name, _) in enumerate(results, start=1):
        print(f"{i}. {name}")
    while True:
        choice = input("Select a result by entering its number (or press 'Q' to search again): ")
        if choice.lower() == 'q':
            return 'search_again'
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(results):
                return results[index][1]  # Return the UUID
        print("Invalid input. Please enter a valid number or 'Q' to search again.")

# Main function
def main():
    filename = 'uuid_data.txt'  # Replace with your filename
    data = read_data(filename)

    if data is not None:
        uuid_data = create_uuid_data(data)

        while True:
            search_term = input("Enter search term (or press 'Q' to quit): ").lower()
            if search_term.lower() == 'q':
                break

            while True:
                matching_results = search_uuids(uuid_data, search_term)
                if not matching_results:
                    print("No matching results found.")
                    break

                selected_uuid = select_result(matching_results)
                if selected_uuid == 'search_again':
                    break
                else:
                    selected_uuid = selected_uuid.split('"', 1)[1]  # Remove text after first speech mark
                    selected_uuid = selected_uuid.split('"')[0]  # Remove final speech mark
                    pyperclip.copy(selected_uuid)
                    print(f"UUID copied to clipboard: {selected_uuid}")

                search_term = input("Enter a new search term (or press 'Q' to search again): ").lower()
                if search_term.lower() == 'q':
                    break

if __name__ == "__main__":
    main()
