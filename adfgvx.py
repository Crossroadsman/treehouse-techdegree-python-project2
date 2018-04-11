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
        print('initialising ADFGVX cipher with keyphrase: {} and grouping: {}'.format(keyphrase, grouping))
        self._create_polybius_square_cipher()
        
        
    def encrypt(self, plaintext):
        '''Takes a string and returns an encrypted string
        '''
        print("encrypting {}".format(plaintext))
        # get the (A,D) (F,G) etc ciphertext using the custom polybius
        print("creating polybius text using custom square")
        self.polybius_text = self.polybius_cipher.encrypt(plaintext)
        print(self.polybius_text)
        # create keyphrase columns and take each character from the 
        # polybius_text and put it into keyphrase_columns
        self._create_keyphrase_columns()
        # sort the columns alphabetically
        print('sorting keyphrase columns alphabetically')
        self.keyphrase_columns.sort()
        print(self.keyphrase_columns)
        # take the letters from the columns and create a single long list
        # of characters
        print('taking each of the column characters and putting into ciphertext string')
        ciphertext = ""
        for column in self.keyphrase_columns:
            for character in column[1:]:
                ciphertext += character
        
        # perform grouping
        grouped_text = self._group_text(ciphertext)
        return grouped_text

    def decrypt(self, ciphertext):
        pass

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
        print('creating polybius cipher with custom values: {}'.format(custom_square))
        self.polybius_cipher = PolybiusSquare(custom_square=custom_square)
        print('created cipher: {}'.format(self.polybius_cipher))

    def _create_keyphrase_columns(self):
        self.keyphrase_columns = []
        print('creating keyphrase columns')
        # 1. reduce the keyphrase to a list of unique characters 
        # (necessary for subsequent sorting)
        # e.g., 'PEOPLE' becomes 'PEOL'
        keyphrase_with_no_duplicates = []
        for character in self.keyphrase:
            if character not in keyphrase_with_no_duplicates: # unique so far
                keyphrase_with_no_duplicates.append(character)
        print('reduced keyphrase {} to no-duplicates {}'.format(self.keyphrase, keyphrase_with_no_duplicates))
        # 2. Add the unique keyphrase characters to the columns:
        # so keyphrase_columns will look like:
        # [[P],[E],[O],[L]]
        for character in keyphrase_with_no_duplicates:
            self.keyphrase_columns.append([character.upper()])
        print('put keyphrase no duplicate letters into columns: {}'.format(self.keyphrase_columns))
        # 3. Split the cipher pairs and put each half into the next available 
        # column:
        print('putting enciphered text into columns')
        i = 0
        for character_pair in self.polybius_text:
            self.keyphrase_columns[i].append(character_pair[0])
            i = (i + 1) % len(keyphrase_with_no_duplicates)
            self.keyphrase_columns[i].append(character_pair[1])
            i = (i + 1) % len(keyphrase_with_no_duplicates)
        print(self.keyphrase_columns)
    



    # Dunder methods
    def __repr__(self):
        print("ADFGVX Cipher (keyphrase: {}, grouping: {})".format(self.keyphrase, self.grouping))

# ----------------------------------------------------------------------

if __name__ == "__main__":
    print("Run tests")

    print("Create ADFGVX Cipher object (with defaults)")
    cipher = Adfgvx()

    print('create plaintext')
    plaintext = 'Attack at 12:00 AM'
    print(plaintext)

    print('encrypt plaintext')
    ciphertext = cipher.encrypt(plaintext)

    print(ciphertext)

