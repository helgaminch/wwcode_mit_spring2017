import math
import random

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1,
    'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1,
    's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}

WORDLIST_FILENAME = "ps3_words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """

    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """

    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.
    word: string
    n: int >= 0
    returns: int >= 0
    """
    points_sum = 0
    for letter in word.lower():
        points_sum += SCRABBLE_LETTER_VALUES[letter]
    second_component = 7 * len(word) - 3 * (n - len(word))
    if second_component > 1:
        return points_sum * second_component
    else:
        return points_sum


def display_hand(hand):
    """
    Displays the letters currently in the hand.
    The order of the letters is unimportant.
    hand: dictionary (string -> int)
    """

    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=' ')
    print()


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """

    hand = {}
    num_vowels = int(math.ceil(n / 3))
    hand['*'] = 1

    for i in range(num_vowels - 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand


def update_hand(hand, word):
    """
    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)
    returns: dictionary (string -> int)
    """
    hand_copy = hand.copy()
    for letter in word.lower():
        if letter in hand_copy.keys():
            hand_copy[letter] -= 1
    new_hand = {}
    for key in hand_copy:
        if hand_copy[key] > 0:
            new_hand[key] = hand_copy[key]
    return new_hand


def are_all_letters_valid(word, hand):
    """
    Returns True if all letters of the word are in hand and False otherwise
    word: string
    hand: dictionary(string -> int)
    returns: boolean
    """
    hand_copy = hand.copy()
    for letter in word.lower():
        if hand_copy.get(letter, 0) == 0:
            return False
        else:
            hand_copy[letter] -= 1
    return True


def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.

    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    if '*' in word:
        for letter in VOWELS:
            new_hand = hand.copy()
            new_hand[letter] = new_hand.get(letter, 0) + 1
            if is_valid_word(word.lower().replace('*', letter), new_hand,
                             word_list):
                return True
        return False

    if word.lower() in word_list and are_all_letters_valid(word, hand):
        return True
    return False


def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.

    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand

    """

    score = 0
    while len(hand) > 0:
        print("Current Hand:", end=' ')
        display_hand(hand)
        user_word = input('Enter word, or "!!" to indicate that'
                          ' you are finished:')
        if user_word == "!!":
            break
        else:
            if is_valid_word(user_word, hand, word_list):
                score += get_word_score(user_word, len(hand))
                print("\"{}\" earned {} points. Total: {} points".format(
                    user_word, get_word_score(user_word, len(hand)),
                    score))
            else:
                print("That is not a valid word. Please choose another word.")
            hand = update_hand(hand, user_word)
        print()

    if len(hand) == 0:
        print("Ran out of letters. Total score for this hand: "
              "{} points".format(score))
    else:
        print("Total score for this hand: {}".format(score))

    return score


def substitute_hand(hand, letter):
    """
    Allow the user to replace all copies of one letter in the hand (chosen by
    user) with a new letter chosen from the VOWELS and CONSONANTS at random.
    The new letter should be different from user's choice, and should not be
    any of the letters already in the hand.
    If user provide a letter not in the hand, the hand should be the same.
    Has no side effects: does not mutate hand.
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    new_hand = hand.copy()

    if letter not in new_hand.keys():
        return new_hand
    letters = set(VOWELS + CONSONANTS)
    letters.remove(letter)
    letters -= set(hand.keys())
    new_letter = random.sample(letters, 1)[0]
    new_hand[new_letter] = new_hand[letter]
    del new_hand[letter]

    return new_hand


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the
      entire series

    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitute option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep
      the better of the two scores for that hand.  This can only be done once
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to
            substitute a letter - you must play whatever hand you just had.

    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    number_of_hands = int(input("Enter total number of hands:"))
    total_score = 0
    is_replay_available = True

    hand = deal_hand(HAND_SIZE)

    while number_of_hands > 0:
        print("Current hand:", end=' ')
        display_hand(hand)

        if input("Would you like to substitute a letter? ") == "yes":
            new_letter = input("Which letter would you like to replace? ")
            hand = substitute_hand(hand, new_letter)
        print()
        result = play_hand(hand, word_list)

        print("----------")

        if is_replay_available:
            wanna_replay = input("Would you like to replay the hand? ")
            print()
            if wanna_replay == "yes":
                is_replay_available = False
                replay_result = play_hand(hand, word_list)
                print("----------")
                if replay_result > result:
                    total_score += replay_result
                hand = deal_hand(HAND_SIZE)
                number_of_hands -= 1
                continue

        total_score += result
        number_of_hands -= 1
        hand = deal_hand(HAND_SIZE)

    print("Total score over all hands is:", total_score)


if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
