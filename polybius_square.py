from ciphers import Cipher

class PolybiusSquare(Cipher):
    '''This is a cipher that fractionates plaintext characters in order to
    represent the text with a smaller set of symbols.
    For a full discussion with worked example, see:
    <https://en.wikipedia.org/wiki/Polybius_square>

    The typical variants take the form of 5x5 or 6x6 squares
    (both modelled here).

    Note that the 5x5 square does not have enough characters to uniquely
    represent every letter in the English alphabet. Two characters need to
    be combined, usually 'c' and 'k' or 'i' and 'j'. This means that when
    decrypting a ciphertext that was encoded with a 5x5 square it is impossible
    to determine which of the combined characters was used in the original
    plaintext.

    This implementation makes explicit this uncertainty by representing each
    occurrence of one of these characters in decoded text with both possible
    characters enclosed in parens.
    '''

    def __init__(self, size=5, shared_character='i', custom_square=None):
        # validation
        ## size
        if type(size) != type(5):
            raise TypeError("Size must be of type 'int'")
        if size < 5:
            raise ValueError("Size must be at least 5")
        if size > 6:
            raise ValueError("Size must be no larger than 6")

        ## shared_character
        if size == 5 and shared_character.lower() not in ['c', 'k', 'i', 'j']:
            raise ValueError("Only shared characters of 'i'/'j' or 'c'/'k' are permitted")


        if custom_square:
            self.column_ids = custom_square[column_ids]
            self.row_ids = custom_square[row_ids]
            self.square = custom_square[square]
            if len(self.square) > 5:
                self.VALID_CHARACTERS += ['0', '1', '2', '3', '4', '5', '6',
                    '7', '8', '9']
        else:
            self.column_ids = None
            self.row_ids = None
            self.square = self._generate_square(size, shared_character)
            if size == 5:
                self.shared_character = shared_character.lower()
            else:
                self.shared_character = None
                self.VALID_CHARACTERS += ['0', '1', '2', '3', '4', '5', '6',
                    '7', '8', '9']


    def encrypt(self, plaintext):
        '''Takes a string and returns an encrypted string
        '''
        plaintext = self._reduce_characters(plaintext)
        plaintext = self._combine_characters(plaintext)
        ciphertext = []
        for character in plaintext:
            ciphertext.append(self._encode_character(character))
        return ciphertext

    def decrypt(self, ciphertext, use_ids=False):
        '''Takes an encrypted string and returns an decrypted string
        '''
        plaintext = ""
        for (row, col) in ciphertext:
            plaintext += self._decode_character(row, col, use_ids)
        plaintext = self._replace_unknowns(plaintext)
        return plaintext




    # Helper methods
    def _generate_square(self, size=5, shared_character='i'):
        '''Creates the polybius_square based on the specified inputs
        (whether to make it 5x5 or 6x6, and which characters to combine for
        5x5 variants)
        '''
        if size == 5:
            if shared_character.lower() in ['i', 'j']:
                return [
                    ['a', 'b', 'c', 'd', 'e'],
                    ['f', 'g', 'h', '?', 'k'],
                    ['l', 'm', 'n', 'o', 'p'],
                    ['q', 'r', 's', 't', 'u'],
                    ['v', 'w', 'x', 'y', 'z'],
                ]
            else: # 'c'/'k'
                return [
                    ['a', 'b', '?', 'd', 'e'],
                    ['f', 'g', 'h', 'i', 'j'],
                    ['l', 'm', 'n', 'o', 'p'],
                    ['q', 'r', 's', 't', 'u'],
                    ['v', 'w', 'x', 'y', 'z'],
                ]
        else: # size == 6
            return [
                ['a', 'b', 'c', 'd', 'e', 'f'],
                ['g', 'h', 'i', 'j', 'k', 'l'],
                ['m', 'n', 'o', 'p', 'q', 'r'],
                ['s', 't', 'u', 'v', 'w', 'x'],
                ['y', 'z', '0', '1', '2', '3'],
                ['4', '5', '6', '7', '8', '9'],
            ]
    
    def _encode_character(self, char):
        '''takes a string containing a single character and looks for it in
        self.square.
        If found, returns a tuple of (row, col) where:
        - if there are col/row ids, the ids are returned as row and col
        - if col/row ids are None, returns the indices of the column and row
        If not found, returns None
        '''
        for row_index in range(len(self.square)):
            for col_index in range(len(self.square[row_index])):
                if char.lower() == self.square[row_index][col_index]:
                    if self.column_ids == None or self.row_ids == None:
                        return (row_index, col_index)
                    else:
                        return (self.row_ids[row_index], self.column_ids[col_index])
        return None

    def _decode_character(self, row, col, use_ids=False):
        '''Takes a reference to a row and col address and determines what
        character should be represented.
        Custom squares (e.g., ADFGVX) use named row and col ids, which can
        be handled by passing in the names of the row and column and setting
        use_ids to True
        ''' 
        if use_ids:
            row_index = self.row_ids.index(row)
            col_index = self.column_ids.index(col)
        else:
            row_index = row
            col_index = col
        return self.square[row_index][col_index]

    def _combine_characters(self, plaintext):
        '''During the encoding process, we need to substitute each occurrence
        of one of the characters that will be combined with a ? (if using a 
        5x5 square)
        '''
        sub_pool = []
        if self.shared_character in ['i', 'j']:
            sub_pool = ['i', 'j']
            substitute = '?'
        elif self.shared_character in ['c', 'k']:
            sub_pool = ['c', 'k']
            substitute = '?'
        else:
            return plaintext
        combined_plaintext = ""
        for letter in plaintext:
            if letter in sub_pool:
                combined_plaintext += substitute
            else:
                combined_plaintext += letter
        return combined_plaintext

    def _replace_unknowns(self, plaintext):
        '''During the decoding process, we need to replace each occurrence of
        ? with the possible value pair (if using 5x5 square)
        '''
        if self.shared_character in ['i', 'j']:
            substitute = '(i/j)'
        elif self.shared_character in ['c', 'k']:
            substitute = '(c/k)'
        else:
            return plaintext
        replaced = ""
        for character in plaintext:
            if character == "?":
                replaced += substitute
            else:
                replaced += character
        return replaced
    
# -----------------------------------------------------------------

if __name__ == "__main__":

    print("Tests:")
    plaintext = "Surprisingly few discotheques provide jukeboxes"

    print("Test 1: defaults")
    cipher = PolybiusSquare()

    ciphertext = cipher.encrypt(plaintext)
    print(ciphertext)

    print("Decrypting {}".format(ciphertext))
    decrypted = cipher.decrypt(ciphertext)
    print(decrypted)

    print("Test 2: size 6")
    cipher = PolybiusSquare(size=6)
    plaintext += "1234567890"
    print(plaintext)

    ciphertext = cipher.encrypt(plaintext)
    print(ciphertext)

    print("Decrypting {}".format(ciphertext))
    decrypted = cipher.decrypt(ciphertext)
    print(decrypted)

    print("Test 3: size=5, shared_character='c'")
    cipher = PolybiusSquare(size=5, shared_character='c')
    plaintext = "Surprisingly few discotheques provide jukeboxes"

    ciphertext = cipher.encrypt(plaintext)
    print(ciphertext)

    print("Decrypting {}".format(ciphertext))
    decrypted = cipher.decrypt(ciphertext)
    print(decrypted)