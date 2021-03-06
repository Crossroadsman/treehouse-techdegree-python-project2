from ciphers import Cipher
from polybius_square import PolybiusSquare


class Adfgvx(Cipher):
    '''This is a fractionating transposition cipher, combining a
    Polybius square with a single columnar transposition.
    For a detailed explanation of the algorithm, together with a worked
    example, see this wikipedia page:
    <https://en.wikipedia.org/wiki/ADFGVX_cipher>

    This implementation has the following options:
    - keyphrase (default='PRIVACY'): the keyphrase to use for column
      transposition
    - grouping (default=5): the number of characters in a group (choose 0 to
                            not implement grouping)
    '''
    def __init__(self, keyphrase='PRIVACY', grouping=5):
        self.keyphrase = keyphrase
        self.grouping = grouping
        self._create_polybius_square_cipher()
        self.PASSTHROUGH_CHARACTERS = []

    def encrypt(self, plaintext):
        '''Takes a string and returns an encrypted string
        '''
        # get the (A,D) (F,G) etc ciphertext using the custom polybius
        self.polybius_text = self.polybius_cipher.encrypt(plaintext)

        # create keyphrase columns and take each character from the
        # polybius_text and put it into keyphrase_columns
        self._populate_keyphrase_columns()

        # sort the columns alphabetically
        self.keyphrase_columns.sort()

        # take the letters from the columns and create a single long list
        # of characters
        ciphertext = ""
        for column in self.keyphrase_columns:
            for character in column[1:]:
                ciphertext += character

        # perform grouping
        grouped_text = self._group_text(ciphertext)
        return grouped_text

    def decrypt(self, ciphertext):
        '''Takes an encrypted string and returns an decrypted string
        '''
        # ungroup text
        ungrouped_text = self._ungroup_text(ciphertext)
        # create sorted columns
        columns = self._create_cols_kp_chars(self.keyphrase)
        sorted_columns = sorted(columns)

        # populate columns
        # (fill each column vertically)
        # (note, some columns will be shorter than others if ciphertext length
        # is not a multiple of unique_length)
        # need to know when repopulating the columns which position each
        # column will be in once unsorted
        text_length = len(ungrouped_text)
        number_of_columns = len(columns)
        characters_in_short_column = text_length // number_of_columns
        if text_length / number_of_columns == text_length // number_of_columns:
            characters_in_full_column = characters_in_short_column
        else:
            characters_in_full_column = characters_in_short_column + 1
        number_of_full_columns = ((text_length - 1) % number_of_columns) + 1

        # suppose key 'PRIVACY'
        # when we start populating the first column, 'A', we can get the index
        # of that value in the string (where all characters are unique)
        # e.g., unique_text.index('A') --> 4
        # thus we know that this will be the column with index 4 (i.e, 5th)
        # if we know that 5 is <= number of full columns then we know this
        # is a full column otherwise it is a short column
        unique_keyphrase = self._uniquify_keyphrase(self.keyphrase)
        char_index = 0
        for i in range(len(sorted_columns)):
            letter = sorted_columns[i][0].upper()
            letter_index_in_keyphrase = unique_keyphrase.index(letter)
            if letter_index_in_keyphrase + 1 <= number_of_full_columns:
                characters_to_append = characters_in_full_column
            else:
                characters_to_append = characters_in_short_column
            for j in range(char_index, char_index + characters_to_append):
                sorted_columns[i].append(ungrouped_text[j])
            char_index = char_index + characters_to_append

        # unsort the columns
        unsorted_columns = self._unsorter(self.keyphrase, sorted_columns)
        # create text string from values in columns
        text = ""
        column_index = 0
        row_index = 1
        while len(text) < len(ungrouped_text):
            character = unsorted_columns[column_index][row_index]
            text += character
            if column_index + 1 > len(unsorted_columns) - 1:
                row_index += 1
            column_index = (column_index + 1) % len(unsorted_columns)

        # decode text
        decoded_text = self.polybius_cipher.decrypt(text, use_ids=True)
        return(decoded_text)

    # Helper methods
    def _create_polybius_square_cipher(self):
        '''Specifies the charateristics for the custom polybius square
        and then creates a PolybiusSquare instance with those inputs
        '''
        row_ids = ['A', 'D', 'F', 'G', 'V', 'X']
        col_ids = row_ids
        square_values = [
            ['n', 'a', '1', 'c', '3', 'h'],
            ['8', 't', 'b', '2', 'o', 'm'],
            ['e', '5', 'w', 'r', 'p', 'd'],
            ['4', 'f', '6', 'g', '7', 'i'],
            ['9', 'j', '0', 'k', 'l', 'q'],
            ['s', 'u', 'v', 'x', 'y', 'z'],
        ]
        custom_square = {'column_ids': col_ids,
                         'row_ids': row_ids,
                         'square': square_values}
        self.polybius_cipher = PolybiusSquare(custom_square=custom_square)

    def _populate_keyphrase_columns(self):
        '''Generates keyphrase columns and then fills each column with the
        individual characters from cipher pairs
        '''
        self.keyphrase_columns = self._create_cols_kp_chars(self.keyphrase)

        i = 0
        unique_length = len(self._uniquify_keyphrase(self.keyphrase))
        for character in self.polybius_text:
            self.keyphrase_columns[i].append(character)
            i = (i + 1) % unique_length

    def _uniquify_keyphrase(self, keyphrase):
        '''for the column sorting to work, the characters in the keyphrase
        must be individually unique (and preserve order)
        e.g., 'PEOPLE' becomes 'PEOL'
        '''
        unique = []
        for character in keyphrase:
            if character not in unique:
                unique.append(character)
        return unique

    def _create_cols_kp_chars(self, keyphrase):
        '''takes the keyphrase and returns a list of lists where each
        inner list is the next sequential unique character from the
        keyphrase.
        e.g., 'PEOPLE' becomes [['P'],['E'],['O'],['L']]
        '''
        unique = self._uniquify_keyphrase(keyphrase)
        columns = []
        for character in unique:
            columns.append([character.upper()])
        return columns

    def _unsorter(self, keyphrase, sorted):
        '''takes a keyphrase of unique values and a list of lists where
        each inner list has a sorted character from keyphrase as the first
        element.
        Returns a new list of lists where each inner list is in the order
        of the keyphrase
        '''
        unsorted = []
        for letter in keyphrase:
            for i in range(len(sorted)):
                if sorted[i][0].lower() == letter.lower():
                    unsorted.append(sorted[i])
                    del sorted[i]
                    break
        return unsorted

    # Dunder methods
    def __repr__(self):
        text = "ADFGVX Cipher (keyphrase: {}, grouping: {})"
        return text.format(self.keyphrase, self.grouping)

# ----------------------------------------------------------------------

if __name__ == "__main__":

    def run_tests(cipher_class, plaintext, tests):
        for key, value in tests.items():
            print('\ntest {}'.format(key))
            kwargs = value
            cipher = cipher_class(**kwargs)
            print("encrypting {}:".format(plaintext))
            encrypted = cipher.encrypt(plaintext)
            print(encrypted)
            print("decrypting {}:".format(encrypted))
            decrypted = cipher.decrypt(encrypted)
            print(decrypted)

    print("Run Test Suite")
    print("==============")
    tests = {
        'a: defaults': {},
        'b: keyphrase only ("People")': {'keyphrase': 'PEOPLE'},
        'c: grouping only (none)': {'grouping': 0},
        'd: grouping only (3)': {'grouping': 3},
        'e: keyphrase ("PEOPLE") and grouping (3)': {'keyphrase': "PEOPLE",
                                                     'grouping': 3}
    }

    test_sets = [
        'the quick brown fox jumps over the lazy dog',
        'numb3r5 and punctuat!0n',
        'Hello Peers'
    ]

    for i in range(len(test_sets)):
        print("\nTest set {}:".format(i + 1))
        print("-----------")
        plaintext = test_sets[i]
        run_tests(Adfgvx, plaintext, tests)
