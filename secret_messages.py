from keyword_cipher import Keyword
from caesar import Caesar
from transposition import Transposition
from adfgvx import Adfgvx
from polybius_square import PolybiusSquare


# Functions
def select_cipher():
    '''ask the user to select a cipher from the available list
    '''
    print("This is the Secret Messages project for the Treehouse Techdegree\n")
    print("These are the current available ciphers:\n")
    for key, value in VALID_CIPHERS.items():
        shortcut = "[" + key.upper() + "]"
        remainder = value['name'][1:].lower()
        print(shortcut + remainder)

    cipher_choice = input("Which cipher would you like to use? ").lower()
    while cipher_choice not in VALID_CIPHERS.keys():
        print("I'm sorry, I didn't recognise that choice. Please try again.")
        print("Valid choices are: ")
        for letter in VALID_CIPHERS.keys():
            print(letter)
        cipher_choice = input("Which cipher would you like to use? ").lower()
    
    return VALID_CIPHERS[cipher_choice]

def get_plaintext():
    '''get the input text from the user
    '''
    plaintext = input("That's an excellent cipher. What's the message? ")
    return plaintext

def select_process():
    '''decide whether to encrypt or decrypt
    '''
    print("Valid processes are:")
    for key, value in VALID_ACTIVITIES.items():
        shortcut = "[" + key.upper() + "]"
        remainder = value[1:].lower()
        print(shortcut + remainder)
    process = input("Which process do you want to use? ")

    while process not in VALID_ACTIVITIES.keys():
        print("I'm sorry, I didn't recognise that choice. Please try again.")
        print("Valid choices are: ")
        for letter in VALID_ACTIVITIES.keys():
            print(letter)
        process = input("Which process do you want to use? ")
    return process

def create_one_time_pad(plaintext):
    '''ask the user if they want to use a one-time pad.
    if so, get the value and validate it
    '''
    line1 = 'Please enter the one-time pad: (or leave blank for none)\n'
    line2 = 'Pad values should be a comma-separated sequence of integers and must'
    line3 = ' be at least as long as the text to be encrypted.\n'
    line4 = 'e.g., if encrypting "Hello", 3,4,17,2,6,9 would be a valid pad: '
    pad_text = line1 + line2 + line3 + line4
    pad_numbers = input(pad_text)
    validated = validate_pad(pad_numbers, len(plaintext))
    while validated['error'] is not None:
        print('Your supplied pad value was invalid:')
        print(validated['error'])
        print('Please try again.')
        pad_numbers = input(pad_text)
        validated = validate_pad(pad_numbers, len(plaintext))
    return pad_numbers

def validate_pad(pad_numbers, min_length):
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
def offset():
    offset_value = int(input('offset value'))
    return ('offset', offset_value)

def num_rails():
    rails = int(input('number of rails'))
    return ('num_rails', rails)

def grouping():
    group = int(input('characters to group by (0 to not group)'))
    return ('grouping', group)

def keyphrase():
    phrase = input('keyphrase')
    return ('keyphrase', phrase)

def size():
    grid = int(input('Square size (valid values are 5 or 6)'))
    return ('size', grid)

def shared_character():
    character = input('Shared character (valid values are "c", "k", "i", "j")')
    return ('shared_character', character)

# Constants

VALID_CIPHERS = {
    'c': {'name': 'Caesar',
          'class': Caesar,
          'parameters': [offset]},
    't': {'name': 'Transposition',
          'class': Transposition,
          'parameters': [num_rails, grouping]},
    'a': {'name': 'ADFGVX',
          'class': Adfgvx,
          'parameters': [num_rails, grouping]},
    'p': {'name': 'Polybius Square',
          'class': PolybiusSquare,
          'parameters': [size, shared_character]},
    'k': {'name': 'Keyword',
          'class': Keyword,
          'parameters': [keyphrase, grouping]},
}
VALID_ACTIVITIES = {
    'e': 'encrypt',
    'd': 'decrypt',
}




# ---------------------------------------------------------------

if __name__ == "__main__":
    
    cipher_id = select_cipher()
    text = get_plaintext()
    process = select_process()
    pad_numbers = create_one_time_pad(text)
    arguments = {}
    for function in cipher_id['parameters']:
        key, value = function()
        arguments[key] = value


    print("You selected to {}, using {} cipher, with {} text and {} pad".format(
        process,
        cipher_id,
        text,
        pad_numbers
    ))

    print("Your arguments are:")
    print(arguments)

    cipher = cipher_id['class'](**arguments)

    if process == 'e':
        processed_text = cipher.encrypt(text)
    else: # process == 'd'
        processed_text = cipher.decrypt(text)
    
    print(processed_text)

