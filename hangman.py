# Problem Set 2, hangman.py
# Hangman Game

import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    returns: string, a word from wordlist at random
    """
    return random.choice(wordlist)

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    """
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    return True


def get_guessed_word(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    """
    result = ""
    for letter in secret_word:
        if letter in letters_guessed:
            result += letter
        else:
            result += "_ "
    return result


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters that represents which letters have not
      yet been guessed.
    """
    result = ""
    for letter in string.ascii_lowercase:
        if letter not in letters_guessed:
            result += letter
    return result


def count_unique_letters(word):
    """
    word: string, assumed to be lowercase
    returns: integer, number of unique symbols in word
    """
    unique = ""
    for letter in word:
        if letter not in unique:
            unique += letter
    return len(unique)


def hangman(secret_word):
    """
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    """
    guesses_remaining = 6
    warnings_remaining = 3
    letters_guessed = []
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is %i letters long." % (len(secret_word)))
    print("You have 3 warnings left.")
    print("------------")

    while guesses_remaining > 0:
        print("You have %i guesses left." % guesses_remaining)
        print("Available letters:", get_available_letters(letters_guessed))

        letter = input("Please guess a letter:").lower()

        # Check user input. Penalize if it is not a letter.
        if len(letter) > 1 or not letter.isalpha():
            if warnings_remaining == 0:
                print("Oops! That is not a valid letter. You now have no warnings left so you lose one guess")
                guesses_remaining -= 1
            else:
                warnings_remaining -= 1
                print("Oops! That is not a valid letter. You now have %i warnings left: %s" %
                      (warnings_remaining, get_guessed_word(secret_word, letters_guessed)))
            print("------------")
            continue

        #Check user input. Penalize if a letter has already been guessed before and is wrong one.
        #If the letter is in secret_word, print warning but don't penalize.
        if letter in letters_guessed:
            if warnings_remaining == 0:
                print("Oops! You've already guessed that letter. You now have no warnings left "
                    "so you lose one guess:", get_guessed_word(secret_word, letters_guessed))
                guesses_remaining -= 1
            else:
                warnings_remaining -= 1
                print("Oops! You've already guessed that letter. You now have %i warnings left: %s" %
                      (warnings_remaining, get_guessed_word(secret_word, letters_guessed)))
            print("------------")
            continue

        letters_guessed.append(letter)

        if letter in secret_word:
            print("Good guess:", get_guessed_word(secret_word, letters_guessed))
        else:
            if letter in "aeiou":
                guesses_remaining -= 2
            else:
                guesses_remaining -= 1
            print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
        print("------------")

        if is_word_guessed(secret_word, letters_guessed):
            print("Congratulations, you won!")
            total_score = guesses_remaining * count_unique_letters(secret_word)
            print("Your total score for this game is:", total_score)
            return

    print("Sorry, you ran out of guesses. The word was", secret_word)
    return


def match_with_gaps(my_word, other_word):
    """
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise 
    """

    my_word = my_word.replace(' ', '')

    if len(my_word) != len(other_word):
        return False
    for i in range(len(my_word)):
        if my_word[i] != "_" and my_word[i] != other_word[i]:
            return False
        if my_word[i] == "_" and other_word[i] in my_word:
            return False
    return True


def show_possible_matches(my_word):
    """
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    """

    result = ""
    for word in wordlist:
        if match_with_gaps(my_word, word):
            result += word + " "
    if len(result) == 0:
        print("No matches found")
        return
    print("Possible word matches are:")
    print(result)


def hangman_with_hints(secret_word):
    """
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman with hints.
    """

    guesses_remaining = 6
    warnings_remaining = 3
    letters_guessed = []
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is %i letters long." % (len(secret_word)))
    print("You have 3 warnings left.")
    print("------------")

    while guesses_remaining > 0:
        print("You have %i guesses left." % guesses_remaining)
        print("Available letters:", get_available_letters(letters_guessed))

        letter = input("Please guess a letter:").lower()

        # Show possible matches if user inputs an asterisk(*)
        if letter == "*":
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            print("------------")
            continue

        # Check user input. Penalize if it is not a letter.
        if len(letter) > 1 or not letter.isalpha():
            if warnings_remaining == 0:
                print("Oops! That is not a valid letter. You now have no warnings left so you lose one guess")
                guesses_remaining -= 1
            else:
                warnings_remaining -= 1
                print("Oops! That is not a valid letter. You now have %i warnings left: %s" %
                      (warnings_remaining, get_guessed_word(secret_word, letters_guessed)))
            print("------------")
            continue

        # Check user input. Penalize if a letter has already been guessed before and is wrong one.
        # If the letter is in secret_word, print warning but don't penalize.
        if letter in letters_guessed:
            if warnings_remaining == 0:
                print("Oops! You've already guessed that letter. You now have no warnings left "
                      "so you lose one guess: %s" % get_guessed_word(secret_word, letters_guessed))
                guesses_remaining -= 1
            else:
                warnings_remaining -= 1
                print("Oops! You've already guessed that letter. You now have %i warnings left: %s" %
                      (warnings_remaining, get_guessed_word(secret_word, letters_guessed)))
            print("------------")
            continue

        letters_guessed.append(letter)

        if letter in secret_word:
            print("Good guess: %s" % (get_guessed_word(secret_word, letters_guessed)))
        else:
            if letter in "aeiou":
                guesses_remaining -= 2
            else:
                guesses_remaining -= 1
            print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
        print("------------")

        if is_word_guessed(secret_word, letters_guessed):
            print("Congratulations, you won!")
            total_score = guesses_remaining * count_unique_letters(secret_word)
            print("Your total score for this game is:", total_score)
            return

    print("Sorry, you ran out of guesses. The word was", secret_word)
    return

if __name__ == "__main__":
    pass
    # To test simple Hangman comment pass and uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

    # To test Hangman with hints re-comment out the above lines and
    # uncomment the following two lines. 
    
    # secret_word = choose_word(wordlist)
    # hangman_with_hints(secret_word)
