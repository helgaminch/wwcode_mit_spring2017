# Problem Set 4B
# Cipher Like Caesar

import string

# HELPER CODE #


def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    # print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    # print("  ", len(wordlist), "words loaded.")
    return wordlist


def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'ps4_words.txt'


class Message(object):
    def __init__(self, text):
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        return self.message_text

    def get_valid_words(self):
        return self.valid_words.copy()

    @staticmethod
    def build_shift_dict(shift):
        """
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        """

        shift_dictionary = {}
        abc_lower = string.ascii_lowercase
        abc_upper = string.ascii_uppercase

        for i in range(26):

            if i + shift < 26:
                shift_dictionary[abc_lower[i]] = abc_lower[i + shift]
                shift_dictionary[abc_upper[i]] = abc_upper[i + shift]
            else:
                shift_dictionary[abc_lower[i]] = abc_lower[i + shift - 26]
                shift_dictionary[abc_upper[i]] = abc_upper[i + shift - 26]

        return shift_dictionary

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shifted_message = ""
        dictionary = self.build_shift_dict(shift)
        for character in self.message_text:
            if character.isalpha():
                shifted_message += dictionary[character]
            else:
                shifted_message += character

        return shifted_message

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = Message.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
       return self.shift

    def get_encryption_dict(self):
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        return self.message_text_encrypted

    def change_shift(self, shift):
        self.shift = shift
        self.encryption_dict = Message.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        Message.__init__(self, text)

    def decrypt_message(self):
        """
            Decrypt self.message_text by trying every possible shift value
            and find the "best" one. 

            Returns: a tuple of the best shift value used to decrypt the message
            and the decrypted message text using that shift value
        """
        best_shift = 0
        max_real_words = 0
        for suggested_shift in range(26):
            real_words_count = 0
            text = self.apply_shift(26 - suggested_shift)
            words = text.split()
            for word in words:
                if is_word(self.valid_words, word):
                    real_words_count += 1
            if real_words_count > max_real_words:
                max_real_words = real_words_count
                best_shift = 26 - suggested_shift
        return best_shift, self.apply_shift(best_shift)


if __name__ == '__main__':


    plain_text = PlaintextMessage("Hello, Python", 5)
    print("Expected Output: Mjqqt, Udymts")
    print("Actual Output:", plain_text.get_message_text_encrypted())
    print("----------")

    plain_text = PlaintextMessage("Keep it short and simple", 22)
    print("Expected Output: Gaal ep odknp wjz oeilha")
    print("Actual Output:", plain_text.get_message_text_encrypted())
    print("----------")

    cipher_text = CiphertextMessage("Mjqqt, Udymts")
    print("Expected Output: (21, 'Hello, Python')")
    print("Actual Output:", cipher_text.decrypt_message())
    print("----------")

    cipher_text = CiphertextMessage("Gaal ep odknp wjz oeilha")
    print("Expected Output: (4, 'Keep it short and simple')")
    print("Actual Output:", cipher_text.decrypt_message())
    print("----------")

    cipher_text = CiphertextMessage(get_story_string())
    decrypt = cipher_text.decrypt_message()
    print("The best shift value is {}\n"
          "Decrypted story:\n{}".format(decrypt[0], decrypt[1]))
