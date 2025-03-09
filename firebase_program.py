import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, db

# Load environment variables from .env file
load_dotenv()

# Get the path to the service account key JSON file from an environment variable
cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH')
database_url = os.getenv('FIREBASE_DATABASE_URL')

if not cred_path:
    raise ValueError("The environment variable 'FIREBASE_CREDENTIALS_PATH' is not set.")

if not database_url:
    raise ValueError("The environment variable 'FIREBASE_DATABASE_URL' is not set.")

# Initialize the Firebase Admin SDK with the credentials and database URL
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': database_url
})

def read_data(path):
    """
    Reads data from the specified path in the Realtime Database.

    Args:
        path (str): The path to the data in the Realtime Database.

    Returns:
        dict: The data read from the database, or None if an error occurred.
    """
    try:
        # Reference to the specified path in the database
        ref = db.reference(path)
        # Get the data from the database
        data = ref.get()
        if isinstance(data, dict):
            return data
        else:
            print("Data is not in the expected dictionary format.")
            return None
    except Exception as e:
        # Print the error message if an exception occurs
        print(f"Error reading data: {e}")
        return None

def get_platforms(data):
    """
    Formats the list of platforms into a comma-separated string.

    Args:
        data (list): A list of platforms.

    Returns:
        str: A comma-separated string of platforms.
    """
    result = ""
    for platform in data:
        result += f"{platform}, "
    # Remove the trailing comma and space
    return result[:-2]

def get_full_game_info(data):
    """
    Formats the full game information into a readable string.

    Args:
        data (dict): A dictionary containing game information.

    Returns:
        str: A formatted string containing the full game information.
    """
    result = ""
    for key, value in data.items():
        result += f"Title: {value['title']}\n"   # Game title
        result += f"Release Year: {value['releaseYear']}\n"    # Release year
        result += f"Platform(s): {get_platforms(value['platform'])}\n\n"    # Platform(s)
    return result

def add_new_game():
    """
    Adds a new game to the database.
    """
    # Get the game information from the user
    title = input("Enter the title of the game: ")
    release_year = input("Enter the release year of the game: ")
    platforms = input("Enter the platforms for the game (comma-separated): ")
    # Split the platforms into a list
    platform_list = platforms.split(",")
    # Create a dictionary with the game information
    game_data = {
        'title': title,
        'releaseYear': release_year,
        'platform': platform_list
    }
    try:
        # Reference to the 'zeldaGames' path in the database
        ref = db.reference('/zeldaGames')
        # Push the new game data to the database
        ref.push(game_data)
        print("Game added successfully.")
    except Exception as e:
        # Print the error message if an exception occurs
        print(f"Error adding game: {e}")

def delete_game():
    """
    Deletes a game from the database.
    """
    # Get the title of the game to delete from the user
    title = input("Enter the title of the game to delete: ")
    try:
        # Reference to the 'zeldaGames' path in the database
        ref = db.reference('/zeldaGames')
        # Get the data from the database
        data = ref.get()
        # Search for the game with the specified title
        for key, value in data.items():
            if value['title'].lower() == title.lower():
                # Delete the game data from the database
                ref.child(key).delete()
                print("Game deleted successfully.")
                break
        else:
            # Print a message if the game is not found
            print("Game not found.")
    except Exception as e:
        # Print the error message if an exception occurs
        print(f"Error deleting game: {e}")

def update_game():
    """
    Updates a game in the database.
    """
    title = input("Enter the title of the game to update: ")
    try:
        # Reference to the 'zeldaGames' path in the database
        ref = db.reference('/zeldaGames')
        # Get the data from the database
        data = ref.get()
        # Search for the game with the specified title
        for key, value in data.items():
            if value['title'].lower() == title.lower():
                # Get the updated game information from the user
                new_title = input("Enter the new title of the game: ")
                new_release_year = input("Enter the new release year of the game: ")
                new_platforms = input("Enter the new platforms for the game (comma-separated): ")
                # Split the platforms into a list
                new_platform_list = new_platforms.split(",")
                # Create a dictionary with the updated game information
                new_game_data = {
                    'title': new_title,
                    'releaseYear': new_release_year,
                    'platform': new_platform_list
                }
                # Update the game data in the database
                ref.child(key).update(new_game_data)
                print("Game updated successfully.")
                break
        else:
            # Print a message if the game is not found
            print("Game not found.")
    except Exception as e:
        # Print the error message if an exception occurs
        print(f"Error updating game: {e}")

def menu():
    """
    Displays the menu options to the user.
    """
    print("0. Exit")
    print("1. Read all data")
    print("2. Read data for a specific game")
    print("3. Add a new game")
    print("4. Delete a game")
    print("5. Update a game")

def read_specific_game(data):
    """
    Reads data for a specific game from the database.

    Args:
        data (dict): The data read from the database.
    """
    # Get the title of the game from the user
    title = input("Enter the title of the game: ")
    # Search for the game with the specified title
    for key, value in data.items():
        if value['title'].lower() == title.lower():
            print()
            # Print the full game information for the specified game
            print(get_full_game_info({key: value}))
            break
    else:
        # Print a message if the game is not found
        print("Game not found.")

def main():
    """
    Main function to run the program.
    """
    running = True

    while running:
    # Read data from the specified path in the database
        data = read_data("/zeldaGames")
        if data is None:
            print("Failed to retrieve data. Exiting.")
            return
    
        # Dictionary to map user choices to functions
        menu_options = {
            1: lambda: print(get_full_game_info(data)),
            2: lambda: read_specific_game(data),
            3: add_new_game,
            4: delete_game,
            5: update_game
        }
    
        # Display the menu options
        menu()
        try:
            # Get the user's choice
            choice = int(input("Enter your choice: "))
            if choice == 0:
                running = False
            elif choice in menu_options:
                menu_options[choice]()
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()