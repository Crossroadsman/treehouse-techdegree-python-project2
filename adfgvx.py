from ciphers import Cipher
from polybius_square import PolybiusSquare

class Adfgvx(Cipher):
    '''This is a fractionating transposition cipher, combining a 
    Polybius square with a single columnar transposition.
    For a detailed explanation of the algorithm, together with a worked example,
    see this wikipedia page:
    <https://en.wikipedia.org/wiki/ADFGVX_cipher>

    This implementation has the following options:
    - keyphrase (default='PRIVACY'): the keyphrase to use for column transposition
    - grouping (default=4): the number of characters in a group (choose 0 to
                            not implement grouping)
    '''
    def __init__(self, keyphrase='PRIVACY', grouping=5):
        self.keyphrase = keyphrase
        self.grouping = grouping
        self._create_polybius_square_cipher()
        
        
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
        # ungroup text
        ungrouped_text = self._ungroup_text(ciphertext)
        # create sorted columns
        columns = self._create_columns_with_keyphrase_chars(self.keyphrase)
        sorted_columns = sorted(columns)
        
        # populate columns
        # (fill each column vertically)
        # (note, some columns will be shorter than others if ciphertext length
        # is not a multiple of unique_length)
        # need to know when repopulating the columns which position each
        # column will be in once unsorted
        ciphertext_length = len(ungrouped_text)
        number_of_columns = len(columns)
        characters_in_short_column = ciphertext_length // number_of_columns
        if ciphertext_length / number_of_columns == ciphertext_length // number_of_columns:
            characters_in_full_column = characters_in_short_column
        else:
            characters_in_full_column = characters_in_short_column + 1
        number_of_full_columns = ((ciphertext_length - 1) % number_of_columns) + 1

        # suppose key 'PRIVACY'
        # when we start populating the first column, 'A', we can get the index
        # of that value in the string (where all characters are unique)
        # e.g., unique_text.index('A') --> 4
        # thus we know that this will be the column with index 4 (i.e, 5th)
        # if we know that 5 is <= number of full columns then we know this
        # is a full column otherwise it is a short column
        unique_keyphrase = self._uniquify_keyphrase(self.keyphrase)
        character_index = 0
        for i in range(len(sorted_columns)):
            letter = sorted_columns[i][0].upper()
            letter_index_in_keyphrase = unique_keyphrase.index(letter)
            if letter_index_in_keyphrase + 1 <= number_of_full_columns:
                characters_to_append = characters_in_full_column
            else:
                characters_to_append = characters_in_short_column
            for j in range(character_index, character_index + characters_to_append):
                sorted_columns[i].append(ungrouped_text[j])
            character_index = character_index + characters_to_append
        
        # unsort the columns
        unsorted_columns = self._unsorter(self.keyphrase, sorted_columns)
        
        # create pairs from values in columns
        pairs = []
        column_index = 0
        row_index = 1
        while len(pairs) < len(ungrouped_text) / 2:
            left = unsorted_columns[column_index][row_index]
            if column_index + 1 > len(unsorted_columns) - 1:
                next_value = unsorted_columns[0][row_index + 1]
            else:
                next_value = unsorted_columns[column_index + 1][row_index]
            right = next_value
            pair = (left, right)
            print(pair)
            pairs.append(pair)
            if column_index + 2 > len(unsorted_columns) - 1:
                row_index += 1
            column_index = (column_index + 2) % len(unsorted_columns)

        # decode pairs
        decoded_text = self.polybius_cipher.decrypt(pairs, use_ids=True)
        # reconstruct string
        # prepend
        print(decoded_text)

    # Helper methods
    def _create_polybius_square_cipher(self):
        '''Specifies the charateristics for the custom polybius square
        and then creates a PolybiusSquare instance with those inputs
        '''
        row_ids = ['A','D','F','G','V','X']
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
        self.keyphrase_columns = self._create_columns_with_keyphrase_chars(self.keyphrase)
        
        # Split the cipher pairs and put each half into the next available 
        # column:
        i = 0
        unique_length = len(self._uniquify_keyphrase(self.keyphrase))
        for character_pair in self.polybius_text:
            self.keyphrase_columns[i].append(character_pair[0])
            i = (i + 1) % unique_length
            self.keyphrase_columns[i].append(character_pair[1])
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

    def _create_columns_with_keyphrase_chars(self, keyphrase):
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
        print("ADFGVX Cipher (keyphrase: {}, grouping: {})".format(self.keyphrase, self.grouping))

# ----------------------------------------------------------------------

if __name__ == "__main__":
    print("Run tests")

    print("Test 1: Create ADFGVX Cipher object (with defaults)")
    cipher = Adfgvx()

    print('create plaintext')
    plaintext = 'Attack at 12:00 AM'
    print(plaintext)

    print('encrypt plaintext')
    ciphertext = cipher.encrypt(plaintext)

    print(ciphertext)

    print('decrypting ciphertext')
    decoded = cipher.decrypt(ciphertext)

    print("Test 2: Create ADFGVX Cipher object (with defaults and non-multiple plaintext)")
    cipher = Adfgvx()

    print('create plaintext')
    plaintext = 'We attack at 12:00 AM'
    print(plaintext)

    print('encrypt plaintext')
    ciphertext = cipher.encrypt(plaintext)

    print(ciphertext)

    print('decrypting ciphertext')
    decoded = cipher.decrypt(ciphertext)

    print("Test 3: Create ADFGVX Cipher object (with custom key)")
    cipher = Adfgvx(keyphrase='HAS REPEATS')

    print('create plaintext')
    plaintext = 'We attack at 12:00 AM'
    print(plaintext)

    print('encrypt plaintext')
    ciphertext = cipher.encrypt(plaintext)

    print(ciphertext)

    print('decrypting ciphertext')
    decoded = cipher.decrypt(ciphertext)

    print("Test 4: Create ADFGVX Cipher object (with custom grouping)")
    cipher = Adfgvx(grouping=4)

    print('create plaintext')
    plaintext = 'We attack at 12:00 AM'
    print(plaintext)

    print('encrypt plaintext')
    ciphertext = cipher.encrypt(plaintext)

    print(ciphertext)

    print('decrypting ciphertext')
    decoded = cipher.decrypt(ciphertext)

