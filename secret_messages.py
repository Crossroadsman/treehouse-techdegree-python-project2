import ciphers
from keyword_cipher import Keyword
from caesar import Caesar
from transposition import Transposition
from adfgvx import Adfgvx
from polybius_square import PolybiusSquare
from one_time_pad import OneTimePad


class Menu:
    # Methods
    def __init__(self):

        # Constants
        self.VALID_CIPHERS = {
            'c': {'name': 'Caesar',
                  'class': Caesar,
                  'parameters': [(self.offset, 3),
                                 (self.grouping, 5)]},
            't': {'name': 'Transposition',
                  'class': Transposition,
                  'parameters': [(self.num_rails, 3),
                                 (self.grouping, 5)]},
            'a': {'name': 'ADFGVX',
                  'class': Adfgvx,
                  'parameters': [(self.keyphrase, 'PRIVACY'),
                                 (self.grouping, 5)]},
            'p': {'name': 'Polybius Square',
                  'class': PolybiusSquare,
                  'parameters': [(self.size, 5),
                                 (self.shared_character, 'i')]},
            'k': {'name': 'Keyword',
                  'class': Keyword,
                  'parameters': [(self.keyphrase, 'PRIVACY'),
                                 (self.grouping, 5)]},
        }
        self.VALID_ACTIVITIES = {
            'e': 'encrypt',
            'd': 'decrypt',
        }
        self._load_menu()

    def _load_menu(self):
        '''Determines which screens to show the user, what values to prompt
        for and how to pass those values into whichever cipher is chosen
        '''
        finished = False
        while not finished:

            # Get inputs from user
            self.cipher_id = self._select_cipher()
            self.text = self._get_plaintext()
            self.process = self._select_process()
            self._create_one_time_pad(self.text, self.cipher_id)
            self.cipher_arguments = self._configure_arguments()

            # create specific cipher
            self.cipher = self.cipher_id['class'](**self.cipher_arguments)

            # set up one time pad (if applicable)
            if self.process == 'e':
                if self.pad is not None:
                    if self.pad.pad_numbers is not None:
                        self.text = self.pad.apply_one_time_pad(
                            self.text,
                            self.cipher)
                    self.processed_text = self.cipher.encrypt(self.text)
            else:  # process == 'd'
                self.processed_text = self.cipher.decrypt(self.text)
                if self.pad is not None:
                    if self.pad.pad_numbers is not None:
                        self.processed_text = self.pad.apply_one_time_pad(
                            self.processed_text,
                            self.cipher,
                            encrypt_mode=False
                        )

            print(self.processed_text)

            again = input("\nWould you like to go again? [y/n] ")
            if again.lower() in ['n', 'no']:
                finished = True

        print("Goodbye")

    def _select_cipher(self):
        '''ask the user to select a cipher from the available list
        '''
        print("This is the Secret Messages project for the Treehouse")
        print("Techdegree\n")
        print("These are the current available ciphers:\n")
        for key, value in self.VALID_CIPHERS.items():
            shortcut = "[" + key.upper() + "]"
            remainder = value['name'][1:].lower()
            print(shortcut + remainder)
        cipher_choice = input("\nWhich cipher would you like to use? ").lower()
        print("you choice: {}".format(cipher_choice))
        while cipher_choice not in self.VALID_CIPHERS.keys():
            print("I'm sorry, I didn't recognise that choice. Try again.")
            print("Valid choices are: ")
            for letter in self.VALID_CIPHERS.keys():
                print(letter)
            cipher_choice = input("Which cipher will you use? ").lower()
        return self.VALID_CIPHERS[cipher_choice]

    def _get_plaintext(self):
        '''get the input text from the user
        '''
        plaintext = input("\nThat's an excellent cipher. What's the message? ")
        return plaintext

    def _select_process(self):
        '''decide whether to encrypt or decrypt
        '''
        print("\nValid processes are:")
        for key, value in self.VALID_ACTIVITIES.items():
            shortcut = "[" + key.upper() + "]"
            remainder = value[1:].lower()
            print(shortcut + remainder)
        process = input("Which process do you want to use? ")

        while process not in self.VALID_ACTIVITIES.keys():
            print("I'm sorry, I didn't recognise that choice. Try again.")
            print("Valid choices are: ")
            for letter in self.VALID_ACTIVITIES.keys():
                print(letter)
            process = input("Which process do you want to use? ")
        return process

    def _create_one_time_pad(self, plaintext, cipher_id):
        '''ask the user if they want to use a one-time pad.
        if so, get the value and validate it
        '''
        line1 = '\nPlease enter the one-time pad: (or leave blank for none)\n'
        line2 = 'Pad values must be:\n'
        line3 = '- a comma-separated sequence of integers, and\n'
        line4 = '- at least as long as the text to be encrypted.\n'
        line5 = 'e.g., for "Hello", 3,4,17,2,6,9 would be a valid pad: '
        pad_text = line1 + line2 + line3 + line4 + line5
        pad_numbers = input(pad_text)
        if input == "":
            self.pad = None
        else:
            self.pad = OneTimePad(pad_numbers,
                                  plaintext,
                                  cipher_id,
                                  self.process)
            while self.pad.error is not None:
                print('Your supplied pad value was invalid:')
                print(self.pad.error)
                print('Please try again.')
                pad_numbers = input(pad_text)
                self.pad = OneTimePad(pad_numbers, plaintext, cipher_id)

    # Functions: Cipher Arguments
    def _configure_arguments(self):
        '''returns a dictionary of argument names and values'''
        # configure arguments to pass to cipher
        arguments = {}
        for pair in self.cipher_id['parameters']:
            function = pair[0]
            default_value = pair[1]
            key, value = function(default_value)
            arguments[key] = value
        return arguments

    def offset(self, default_value):
        print("\nChoose an offset value")
        input_text = 'Or leave blank for default ({}) '.format(default_value)
        offset_value = input(input_text)
        if offset_value == '':
            return ('offset', default_value)
        else:
            return ('offset', int(offset_value))

    def num_rails(self, default_value):
        print('\nChoose the number of rails')
        rails = input('Or leave blank for default ({}) '.format(default_value))
        if rails == '':
            return ('num_rails', default_value)
        else:
            return ('num_rails', int(rails))

    def grouping(self, default_value):
        if self.process == 'd':
            lines = [
                "\nAre your characters grouped into **same-sized** chunks?",
                "",
                "Important: if you are using an algorithm that preserves word",
                "boundaries when `grouping=0` then enter 'n'. Only enter 'y'",
                "if spaces are caused by setting the grouping parameter to a",
                "value other than 0."
            ]
            for line in lines:
                print(line)
            group = input('[y/N] ')
            if group.lower() in [' ', 'y', 'yes']:
                return ('grouping', 1)
            else:
                return ('grouping', 0)
        else:
            print("")
            group = input('How many characters to group by (0 to not group) ')
            if group == '':
                group = 0
            try:
                group = int(group)
            except:
                raise ValueError("Invalid input. Should be an int")
            return ('grouping', group)

    def keyphrase(self, default_value):
        print("\nChoose a keyphrase ")
        input_text = 'Or leave blank for default ({}) '.format(default_value)
        phrase = input(input_text)
        if phrase == '':
            return ('keyphrase', default_value)
        else:
            return ('keyphrase', phrase)

    def size(self, default_value):
        grid = int(input('\n Choose a square size (valid values are 5 or 6) '))
        self.grid_size = grid
        return ('size', grid)

    def shared_character(self, default_value):
        if self.grid_size:
            print("\nChoose a shared character")
            character = input('(valid values are: "c", "k", "i", "j") ')
            return ('shared_character', character)

# ---------------------------------------------------------------

if __name__ == "__main__":

    menu = Menu()
