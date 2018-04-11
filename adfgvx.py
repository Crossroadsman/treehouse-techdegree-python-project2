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
    def __init__(self, keyphrase='PRIVACY', grouping=4):
        self.keyphrase = keyphrase
        self.grouping = grouping
        self._create_polybius_square_cipher()
        
        
    def encrypt(self, plaintext):
        # get the (A,D) (F,G) etc ciphertext using the custom polybius
        polybius_text = self.polybius_cipher.encrypt(plaintext)
        # take each character from the polybius_text and put it into
        # keyphrase_columns
        self._create_keyphrase_columns()
        # sort the columns alphabetically
        self.keyphrase_columns.sort()
        # take the letters from the columns and create a single long list
        # of characters
        ciphertext = ""
        for column in self.keyphrase_columns:
            for character in column[1:]:
                ciphertext += character
        
        # perform grouping

    def decrypt(self, ciphertext):
        pass

    # Helper methods
    def _create_polybius_square_cipher(self):
        '''creates a custom polybius square
        '''
        (row_ids, col_ids) = ['A','D','F','G','V','X']
        square_values = [
            ['n', 'a', '1', 'c', '3', 'h'],
            ['8', 't', 'b', '2', 'o', 'm'],
            ['e', '5', 'w', 'r', 'p', 'd'],
            ['4', 'f', '6', 'g', '7', 'i'],
            ['9', 'j', '0', 'k', 'l', 'q'],
            ['s', 'u', 'v', 'x', 'y', 'z'],
        ]
        custom_square = (row_ids, col_ids, square_values)
        self.polybius_cipher = PolybiusSquare(custom_square=custom_square)

    def _create_keyphrase_columns()
        self.keyphrase_columns = []

        # 1. reduce the keyphrase to a list of unique characters 
        # (necessary for subsequent sorting)
        # e.g., 'PEOPLE' becomes 'PEOL'
        keyphrase_with_no_duplicates = []
        for character in self.keyphrase:
            if character not in keyphrase_with_no_duplicates: # unique so far
                keyphrase_with_no_duplicates.append(character)
        
        # 2. Add the unique keyphrase characters to the columns:
        # so keyphrase_columns will look like:
        # [[P],[E],[O],[L]]
        for character in keyphrase_with_no_duplicates:
            self.keyphrase_columns.append([character.upper()])
        
        # 3. Split the cipher pairs and put each half into the next available 
        # column:
        i = 0
        for character_pair in self.polybius_text:
            self.keyphrase_columns[i].append(character_pair[0])
            i = (i + 1) % len(keyphrase_with_no_duplicates)
            self.keyphrase_columns[i].append(character_pair[1])
            i = (i + 1) % len(keyphrase_with_no_duplicates)
    



    # Dunder methods
    def __repr__(self):
        print("ADFGVX Cipher (keyphrase: {}, grouping: {})".format(self.keyphrase, self.grouping))


if __name__ == "__main__":
    print("Run tests")
    #print("Create Transposition Cipher object (with defaults)")
    #cipher = Transposition()

    #print('create plaintext')
    #plaintext = 'hello, world'
    #print(plaintext)

    #print('encrypt plaintext')
    #ciphertext = cipher.encrypt(plaintext)

    #print(ciphertext)

