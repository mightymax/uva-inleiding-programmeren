# Name: Mees Lindeman - 12231207
# Module 4

# Assignment: Hangman
# This program lets you play a game called Hangman, it chooses a word and it's up to you
# to guess this word by guessing the single letters.

import random

class Lexicon:
    def __init__(self, word_length):
        assert word_length >= 1 and word_length <= 28, "Invalid word length for Lexicon"
        lexicon = open("dictionary.txt", 'r')
        self._usable_words = []
        for word in lexicon:        
            word = word.strip()
            if (len(word)) == word_length:
                self._usable_words.append(word)

    # chooses a random word from the list
    def get_word(self):
        return random.choice(self._usable_words)

class Hangman:
    
    def __init__(self, word, number_guesses):
        self._word = word
        self._number_guesses = number_guesses
        self._already_guessed = []
        self._current_pattern = "_" * (len(self._word))
    
    # sets condition to keep the game running
    def is_running(self):
        if self._number_guesses == 0 or self._current_pattern == self._word:
            return False
        else:
            return True

    # provides the number of guesses left
    def guesses_left(self):
        return self._number_guesses 
        
    def assert_valid_letter(self, letter):
        letter = str(letter)
        assert letter.isalpha(), "This is not a letter"
        assert len(letter) == 1, "Please enter one letter only"
        assert letter not in self._already_guessed, "You've already guessed this letter"
        assert letter.lower(), "Letter must be lowercase"
        return letter.lower()
    
    # validates if the input is in a correct form as a letter
    def is_valid_guess(self, letter):
        letter = str(letter)
        try:
            return self.assert_valid_letter(letter)
        except AssertionError as msg:
            print(msg)
            return False

    # checks if the guessed letter is in word
    def guess(self, letter):
        self._letter = self.assert_valid_letter(letter)
        self._already_guessed.append(letter)
        self._number_guesses -= 1
        return letter in self._word
    
    # form the current pattern to see which letters are correct and what needs to be guessed
    def current_pattern(self):
        for i in range(len(self._word)):
            if self._word[i] == self._letter:
                self._current_pattern = self._current_pattern[:i] + self._letter + self._current_pattern[i+1:]
        return self._current_pattern
    
    # sets condition to winning the game
    def won(self):
        if self._current_pattern == self._word:
            return True
        else:
            return False

# Helper function to aks for a valid number:
def ask_for_valid_number(
    prompt = "Please enter a valid number:", 
    min_num = False, msg_min_num = "Your number must be larger than %d.", 
    max_num = False, msg_max_num = "Your number must be less than %d."
):
    # prompt and re-prompt for word length
    validInput = False
    while False == validInput:
        num = input(f"{prompt}\n")
        if not num.isdigit():
            print (f"`{word_length}` is not a valid number!")
        elif not min_num == False and int(num) < int(min_num):
            print (msg_min_num % int(min_num))
        elif not max_num == False and int(num) > int(max_num):
            print (msg_max_num % int(max_num))
        else:
            validInput = True
            return int(num)

def main():
    print("WELCOME TO HANGMAN ツ")

    word_length = ask_for_valid_number(
        "What length of word would you like to play with?", 
        min_num=1, 
        max_num=44, msg_max_num="No words are longer than %d letters!")

    number_guesses = ask_for_valid_number(
        "How many guesses are allowed?", 
        min_num=1, msg_min_num = "Negative or zero (<%d) guesses make no sense.",
        max_num=25, msg_max_num = "Anyone can win this game given more than %d guesses."
    )

    lexicon = Lexicon(word_length)

    # run an infinite number of games
    while True:

        # game set-up
        word = lexicon.get_word()
        game = Hangman(word, number_guesses)

        # allow guessing and provide guesses to the game
        while game.is_running():

            # prompt and re-prompt for single letter
            letter = input(f"Guess a letter ({game.guesses_left()} left): ")
            if not game.is_valid_guess(letter):
                continue

            # provide feedback
            if game.guess(letter):
                print("It's in the word! :))")
            else:
                print("That's not in the word :(")
        
            print(game.current_pattern())

        # after game ends, present the conclusion
        if game.won():
            print("Whoa, you won!!! Let's play again.")
        else:
            print(f"Sad, you lost ¯\_(ツ)_/¯. This was your word: {word}")


if __name__ == '__main__':
    try:
        main();
    except KeyboardInterrupt:
        print(f"\nSad, to see you go ¯\(°_o)/¯.")
    except:
        print(f"Bugger, something unexpected happened ¯\(°_o)/¯.")
