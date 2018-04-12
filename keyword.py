from ciphers import Cipher


class Keyword(Cipher):
    '''This is a monoalphabetic substitution cipher, where a keyword is used
    as the key which determines the substitution characters.
    For a detailed explanation of the algorithm, together with a worked
    example, see this wikipedia page:
    <https://en.wikipedia.org/wiki/Keyword_cipher>

    This implementation has the following options:
    - keyphrase (default='PRIVACY'): the keyphrase to use for column
      transposition
    - grouping (default=5): the number of characters in a group (choose 0 to
                            not implement grouping)
    '''
    def __init__(self, keyphrase='PRIVACY', grouping=5):
        self.keyphrase = self._valid_keyphrase(keyphrase)
        self.grouping = grouping

    def encrypt(self, plaintext):
        '''Takes a string and returns an encrypted string
        '''
        substitution_list = self._alphabet_from_keyphrase(self.keyphrase)
        # create a mapping from plaintext to ciphertext
        character_map = self._map_characters(self.keyphrase, substitution_list)

        # reduce plaintext to valid characters
        plaintext = self._reduce_characters(plaintext)
        plaintext = plaintext.lower()

        ciphertext = ""
        for character in plaintext:
            ciphertext += character_map[character]

        grouped_text = self._group_text(ciphertext)
        return grouped_text

    def decrypt(self, ciphertext):
        '''Takes an encrypted string and returns an decrypted string
        '''
        # ungroup text
        ungrouped_text = self._ungroup_text(ciphertext)

        substitution_list = self._alphabet_from_keyphrase(self.keyphrase)
        character_map = self._map_characters(self.keyphrase, substitution_list)
        character_map = self._invert_dict(character_map)

        plaintext = ""
        for character in ungrouped_text:
            plaintext += character_map[character]

        #return decoded_text
        return plaintext

    # Helper methods
    def _non_keyphrase_characters(self, keyphrase):
        '''creates an ordered list of all the VALID_CHARACTERS that aren't
        in the keyphrase
        '''
        char_list = []
        for character in self.VALID_CHARACTERS:
            if character.lower() not in keyphrase:
                char_list.append(character.lower())
        return char_list

    def _valid_keyphrase(self, keyphrase):
        '''takes a user-provided keyphrase and reduces it to a unique
        list of only valid characters
        '''
        keyphrase = self._reduce_characters(keyphrase)
        keyphrase = self._uniquify_keyphrase(keyphrase)
        keyphrase = [char.lower() for char in keyphrase]
        return keyphrase

    def _alphabet_from_keyphrase(self, keyphrase):
        '''takes a validated keyphrase and creates a full alphabet to be used 
        as the substitution list for the cipher
        '''
        other_characters = self._non_keyphrase_characters(keyphrase)
        other_characters = [char.lower() for char in other_characters]
        substitution_list = keyphrase + other_characters
        return substitution_list
    
    def _map_characters(self, keyphrase, substitution_list):
        '''creates a mapping of each character in VALID_CHARACTERS to
        a character in the substitution_list (which is the reduced keyword
        followed by all the remaining ordered characters from VALID_CHARACTERS)
        '''
        character_map = {}
        for i in range(len(self.VALID_CHARACTERS)):
            character_map[self.VALID_CHARACTERS[i]] = substitution_list[i]
        return character_map
    
    def _invert_dict(self, dictionary):
        '''switches keys and values for a dictionary. For this cipher values
        in the dictionary will always be unique so will be valid keys on 
        inversion.
        '''
        return {value: key for key, value in dictionary.items()}


    # Dunder methods
    def __repr__(self):
        text = "Keyword Cipher (keyphrase: {}, grouping: {})"
        print(text.format(self.keyphrase, self.grouping))

# ----------------------------------------------------------------------

if __name__ == "__main__":
    print("Run tests")

    print("Test 1: Create Keyword Cipher object (with defaults)")
    cipher = Keyword()

    print('create plaintext')
    plaintext = 'Knowledge is power'
    print(plaintext)

    print('encrypt plaintext')
    ciphertext = cipher.encrypt(plaintext)

    print(ciphertext)

    print('decrypting ciphertext')
    decoded = cipher.decrypt(ciphertext)
    print(decoded)

    print("Test 2: Create Keyword Cipher object")
    print("with defaults and non-multiple plaintext)")
    cipher = Keyword()

    print('create plaintext')
    plaintext = 'Knowledge is power'
    print(plaintext)

    print('encrypt plaintext')
    ciphertext = cipher.encrypt(plaintext)

    print(ciphertext)

    print('decrypting ciphertext')
    decoded = cipher.decrypt(ciphertext)
    print(decoded)

    print("Test 3: Create Keyword Cipher object (with custom key)")
    #cipher = Keyword(keyphrase='HAS REPEATS')
    cipher = Keyword(keyphrase='KRYPTOS')

    print('create plaintext')
    plaintext = 'Knowledge is power'
    print(plaintext)

    print('encrypt plaintext')
    ciphertext = cipher.encrypt(plaintext)

    print(ciphertext)

    print('decrypting ciphertext')
    decoded = cipher.decrypt(ciphertext)
    print(decoded)

    print("Test 4: Create Keyword Cipher object (with custom grouping)")
    cipher = Keyword(grouping=4)

    print('create plaintext')
    plaintext = 'Knowledge is power'
    print(plaintext)

    print('encrypt plaintext')
    ciphertext = cipher.encrypt(plaintext)

    print(ciphertext)

    print('decrypting ciphertext')
    decoded = cipher.decrypt(ciphertext)
    print(decoded)
