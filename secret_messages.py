import ciphers
from keyword_cipher import Keyword
from caesar import Caesar
from transposition import Transposition
from adfgvx import Adfgvx
from polybius_square import PolybiusSquare


class Menu:
    # Methods
    def __init__(self):
        print('Initialising Menu instance')
        
        # Constants
        self.VALID_CIPHERS = {
            'c': {'name': 'Caesar',
                'class': Caesar,
                'parameters': [(self.offset, 3)]},
            't': {'name': 'Transposition',
                'class': Transposition,
                'parameters': [(self.num_rails, 3), (self.grouping, 5)]},
            'a': {'name': 'ADFGVX',
                'class': Adfgvx,
                'parameters': [(self.keyphrase, 'PRIVACY'), (self.grouping, 5)]},
            'p': {'name': 'Polybius Square',
                'class': PolybiusSquare,
                'parameters': [(self.size, 5), (self.shared_character, 'i')]},
            'k': {'name': 'Keyword',
                'class': Keyword,
                'parameters': [(self.keyphrase, 'PRIVACY'), (self.grouping, 5)]},
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
        print("Loading menu")
        
        finished = False

        print("Entering UI loop")
        while not finished:

            # Get inputs from user
            self.cipher_id = self._select_cipher()
            self.text = self._get_plaintext()
            self.process = self._select_process()
            self.pad_numbers = self._create_one_time_pad(self.text)
            self.cipher_arguments = self._configure_arguments()

            # create specific cipher
            print("ARGS:")
            for key,value in self.cipher_arguments.items():
                print("{}: {}".format(key,value))
            self.cipher = self.cipher_id['class'](**self.cipher_arguments)

            # set up one time pad (if applicable)
            if self.process == 'e':
                if self.pad_numbers is not None:
                    self.text = self.cipher.apply_one_time_pad(
                        self.pad_numbers, 
                        self.text)
                self.processed_text = self.cipher.encrypt(self.text)
            else:  # process == 'd'
                self.processed_text = self.cipher.decrypt(self.text)
                if self.pad_numbers is not None:
                    self.processed_text = self.cipher.apply_one_time_pad(
                        self.pad_numbers,
                        self.processed_text,
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
            print("I'm sorry, I didn't recognise that choice. Please try again.")
            print("Valid choices are: ")
            for letter in self.VALID_CIPHERS.keys():
                print(letter)
            cipher_choice = input("Which cipher would you like to use? ").lower()
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
            print("I'm sorry, I didn't recognise that choice. Please try again.")
            print("Valid choices are: ")
            for letter in self.VALID_ACTIVITIES.keys():
                print(letter)
            process = input("Which process do you want to use? ")
        return process

    def _create_one_time_pad(self, plaintext):
        '''ask the user if they want to use a one-time pad.
        if so, get the value and validate it
        '''
        line1 = '\nPlease enter the one-time pad: (or leave blank for none)\n'
        line2 = 'Pad values must be:\n'
        line3 = '- a comma-separated sequence of integers, and\n'
        line4 = '- at least as long as the text to be encrypted.\n'
        line5 = 'e.g., if encrypting "Hello", 3,4,17,2,6,9 would be a valid pad: '
        pad_text = line1 + line2 + line3 + line4 + line5
        pad_numbers = input(pad_text)
        validated = self._validate_pad(pad_numbers, len(plaintext))
        while validated['error'] is not None:
            print('Your supplied pad value was invalid:')
            print(validated['error'])
            print('Please try again.')
            pad_numbers = input(pad_text)
            validated = self._validate_pad(pad_numbers, len(plaintext))
        return validated['pad_numbers']

    def _validate_pad(self, pad_numbers, min_length):
        '''takes a user-supplied prospective one-time pad and determines its
        validity.
        Returns a dictionary with two keys, `error` and `pad_numbers`.
        If the pad is valid, error will be None and pad_numbers will be the values
        (None can be a valid value for pad_numbers).
        If the pad is invalid, error will be a description of the error and
        pad_numbers will be None
        '''
        # check if pad is blank
        if pad_numbers == '':
            error = None
            pad_numbers = None
            return {'error': error,
                    'pad_numbers': pad_numbers}

        # turn comma-separated into list of values
        pad_numbers = pad_numbers.split(',')

        # try to convert the list elements into ints
        try:
            pad_numbers = [int(element) for element in pad_numbers]
        except ValueError:
            error = 'Invalid characters in pad, should only contain ints'
            pad_numbers = None
            return {'error': error,
                    'pad_numbers': pad_numbers}

        # check the length is sufficient
        if len(pad_numbers) < min_length:
            error = 'Too short, pad must be at least as long as plaintext'
            pad_numbers = None
        else:
            error = None
        return {'error': error,
                'pad_numbers': pad_numbers}

    # Functions: Cipher Arguments
    def _configure_arguments(self):
        '''returns a dictionary of argument names and values'''
        # configure arguments to pass to cipher
        arguments = {}
        for pair in self.cipher_id['parameters']:
            function = pair[0]
            default_value = pair[1]
            state = {'text': self.text,
                    'process': self.process,
                    'pad_numbers': self.pad_numbers,
            }
            key, value = function(default_value, state)
            arguments[key] = value
        return arguments

    def offset(self, default_value, state):
        print("\nChoose an offset value")
        offset_value = input('Or leave blank for default ({}) '.format(default_value))
        if offset_value == '':
            return ('offset', default_value)
        else:
            return ('offset', int(offset_value))

    def num_rails(self, default_value, state):
        print('\nChoose the number of rails')
        rails = input('Or leave blank for default ({}) '.format(default_value))
        if rails == '':
            return ('num_rails', default_value)
        else:
            return ('num_rails', rails)

    def grouping(self, default_value, state):
        if state['process'] == 'd':
            return ('grouping', default_value)
        else:
            group = input('\nHow many characters to group by (0 to not group) ')
            if group == '':
                group = 0
            try:
                group = int(group)
            except:
                raise ValueError("Invalid input. Should be an int")
            return ('grouping', group)

    def keyphrase(self, default_value, state):
        print("\nChoose a keyphrase ")
        phrase = input('Or leave blank for default ({}) '.format(default_value))
        if phrase == '':
            return ('keyphrase', default_value)
        else:
            return ('keyphrase', phrase)

    def size(self, default_value, state):
        grid = int(input('\n Choose a square size (valid values are 5 or 6) '))
        self.grid_size = grid
        return ('size', grid)

    def shared_character(self, default_value, state):
        if self.grid:
            print("\nChoose a shared character")
            character = input('(valid values are: "c", "k", "i", "j") ')
            return ('shared_character', character)

# ---------------------------------------------------------------

if __name__ == "__main__":

    menu = Menu()
