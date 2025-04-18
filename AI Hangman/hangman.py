import os
import random
import time
from typing import List, Set, Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ASCII art for hangman stages
HANGMAN_STAGES = [
    '''
       --------
       |      |
       |      
       |    
       |     
       |    
    ''',
    '''
       --------
       |      |
       |      O
       |    
       |     
       |    
    ''',
    '''
       --------
       |      |
       |      O
       |      |
       |     
       |    
    ''',
    '''
       --------
       |      |
       |      O
       |     /|
       |     
       |    
    ''',
    '''
       --------
       |      |
       |      O
       |     /|\\
       |     
       |    
    ''',
    '''
       --------
       |      |
       |      O
       |     /|\\
       |     / 
       |    
    ''',
    '''
       --------
       |      |
       |      O
       |     /|\\
       |     / \\
       |    
    '''
]

class HangmanGame:
    """A class representing a Hangman game with AI-powered word generation."""
    
    def __init__(self) -> None:
        """Initialize the Hangman game with default values."""
        self.words: List[str] = []
        self.current_word: str = ""
        self.guessed_letters: Set[str] = set()
        self.remaining_tries: int = 6
        
        # Get API key from environment variable
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)

    def generate_words(self, topic: str) -> bool:
        """
        Generate words based on the given topic using Gemini API.
        
        Args:
            topic: The topic to generate words for
            
        Returns:
            bool: True if words were generated successfully, False otherwise
        """
        try:
            model = genai.GenerativeModel("gemini-2.0-flash-lite")
            
            prompt = f"""Generate a list of 30 unique words suitable for a Hangman game. 
The words must be between 4 and 9 letters in length and related to the topic: {topic}.
Your response must only be the list of generated words. 
Format the output with each word in ALL CAPS on a separate line."""
            
            response = model.generate_content(prompt)
            
            if hasattr(response, 'text'):
                self.words = [word.strip() for word in response.text.split('\n') 
                            if word.strip() and 4 <= len(word.strip()) <= 9]
                return len(self.words) > 0
            return False
            
        except Exception as e:
            print(f"Error generating words: {str(e)}")
            return False

    def select_new_word(self) -> bool:
        """
        Select a new word from the available words.
        
        Returns:
            bool: True if a new word was selected, False otherwise
        """
        if not self.words:
            return False
        self.current_word = random.choice(self.words)
        self.words.remove(self.current_word)
        self.guessed_letters = set()
        self.remaining_tries = 6
        return True

    def display_word(self) -> str:
        """
        Display the word with guessed letters revealed.
        
        Returns:
            str: The word with unguessed letters replaced by underscores
        """
        return ' '.join(letter if letter in self.guessed_letters else '_' 
                       for letter in self.current_word)

    def make_guess(self, letter: str) -> str:
        """
        Process a letter guess.
        
        Args:
            letter: The letter being guessed
            
        Returns:
            str: A message indicating the result of the guess
        """
        letter = letter.upper()
        if not letter.isalpha():
            return "Please enter a valid letter!"
            
        if letter in self.guessed_letters:
            return "You already guessed that letter!"
        
        self.guessed_letters.add(letter)
        
        if letter not in self.current_word:
            self.remaining_tries -= 1
            return f"Wrong guess! {self.remaining_tries} tries remaining."
        
        return "Good guess!"

    def is_word_complete(self) -> bool:
        """
        Check if all letters in the word have been guessed.
        
        Returns:
            bool: True if all letters have been guessed, False otherwise
        """
        return all(letter in self.guessed_letters for letter in self.current_word)

def get_valid_input(prompt: str, valid_options: Set[str]) -> str:
    """
    Get valid user input from a set of options.
    
    Args:
        prompt: The prompt to display to the user
        valid_options: Set of valid input options
        
    Returns:
        str: The valid user input
    """
    while True:
        choice = input(prompt).strip()
        if choice in valid_options:
            return choice
        print(f"Please enter one of: {', '.join(valid_options)}")

def main() -> None:
    """Main game loop."""
    try:
        game = HangmanGame()
        
        while True:
            print("\n=== HANGMAN GAME ===")
            print("1. Start new game with topic")
            print("2. Exit")
            
            choice = get_valid_input("Enter your choice (1-2): ", {"1", "2"})

            if choice == "2":
                print("Thanks for playing!")
                break
                
            topic = input("Enter a topic for the words (e.g., 'animals', 'countries'): ").strip()
            if not topic:
                print("Topic cannot be empty!")
                continue
                
            print(f"\nGenerating words for topic: {topic}")
            
            if not game.generate_words(topic):
                print("Failed to generate words. Please try again.")
                continue

            print(f"Generated {len(game.words)} words! Let's play!")

            while game.words or game.current_word:
                if not game.current_word:
                    if not game.select_new_word():
                        print("\nNo more words available!")
                        break
                    print("\nNew word selected!")

                print(HANGMAN_STAGES[6 - game.remaining_tries])
                print(f"\nWord: {game.display_word()}")
                print(f"Guessed letters: {', '.join(sorted(game.guessed_letters))}")
                print(f"Remaining tries: {game.remaining_tries}")
                
                guess = input("Enter a letter (or 'quit' to exit, 'next' for new word): ").strip().upper()
                
                if guess == 'QUIT':
                    print("Thanks for playing!")
                    return
                elif guess == 'NEXT':
                    if game.words:
                        game.select_new_word()
                        continue
                    else:
                        print("No more words available!")
                        break
                elif len(guess) != 1 or not guess.isalpha():
                    print("Please enter a single letter!")
                    continue

                result = game.make_guess(guess)
                print(result)

                if game.is_word_complete():
                    print(f"\nCongratulations! You guessed the word: {game.current_word}")
                    time.sleep(1)
                    game.current_word = ""
                elif game.remaining_tries == 0:
                    print(f"\nGame Over! The word was: {game.current_word}")
                    time.sleep(1)
                    game.current_word = ""
                time.sleep(0.5)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return

if __name__ == "__main__":
    main()
