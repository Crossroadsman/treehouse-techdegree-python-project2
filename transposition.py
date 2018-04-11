from ciphers import Cipher


class Transposition(Cipher):
    '''This is a transposition cipher, specifically a 'rail fence' cipher,
    where plaintext is written up and down the 'rails' of an imaginary fence.
    For detailed explanation of the algorithm, together with a worked example,
    see this wikipedia page:
    <https://en.wikipedia.org/wiki/Transposition_cipher#Rail_Fence_cipher>

    This implementation has the following options:
    - num_rails (default=3): the number of fence rails
    - grouping (default=5): the number of characters in a group (choose 0 to
                            not implement grouping)
    '''
    def __init__(self, num_rails=3, grouping=5):
        self.num_rails = num_rails
        self.grouping = grouping

    def encrypt(self, plaintext):
        '''Takes a string and returns an encrypted string
        '''
        plaintext = self._reduce_characters(plaintext).lower()
        self._initialise_rails(plaintext)
        self._add_plaintext_to_rails(plaintext)
        flattened_text = self._flatten_railtext()
        grouped_text = self._group_text(flattened_text)
        return grouped_text

    def decrypt(self, ciphertext):
        '''Takes an encrypted string and returns an decrypted string
        '''
        pass

    # Helper methods
    def _initialise_rails(self, plaintext):
        '''creates the appropriate number of empty rails with the length
        of the plaintext
        '''
        blanks = ["" for _ in range(len(plaintext))]
        self.rails = [blanks[:] for rail in range(self.num_rails)]

    def _add_plaintext_to_rails(self, plaintext):
        '''Write the plaintext into the rails, for example, with three rails
        and plaintext of 'HELLO':
        [['H', '',  '',  '',  'O'],
         ['',  'E', '',  'L', '' ],
         ['',  '',  'L', '',  '' ],
        ]
        '''
        rail_number = 0
        down = True
        for i in range(len(plaintext)):
            # write the i'th character in plaintext to the i'th position
            # of the current rail
            self.rails[rail_number][i] = plaintext[i]

            if down:
                # check if at bottom rail, if so, switch to up
                if rail_number == self.num_rails - 1:
                    down = False
                    rail_number -= 1
                else:
                    rail_number += 1
            else:
                # check if at top rail, if so, switch to down
                if rail_number == 0:
                    down = True
                    rail_number += 1
                else:
                    rail_number -= 1

    def _flatten_railtext(self):
        '''Flattens down the multiple lists of characters into a single string
        '''
        output = ""
        for rail in self.rails:
            rail = "".join(rail)
            output += rail
        return output

    def _group_text(self, text):
        '''Splits the long single 'word' of characters into groups of a
        specified size
        '''
        if self.grouping > 0:
            grouped = ""
            for i in range(len(text)):
                if i % self.grouping == 0 and i != 0:
                    grouped += " "
                grouped += text[i]
            return grouped
        else:
            return text

    def _pretty_print_rails(self):
        '''Convenience method for when debugging, displays the text in
        the rails in a readable fashion
        '''
        print('-' * 50)
        for rail in self.rails:
            print(rail)
        print('-' * 50)

    # Dunder methods
    def __repr__(self):
        text = "Transposition (rail fence) Cipher (rails: {}, grouping: {})"
        print(text.format(self.num_rails, self.grouping))

# -----------------------------------------------------------------

if __name__ == "__main__":
    print("Run tests")
    plaintext = 'WE ARE DISCOVERED. FLEE AT ONCE'

    print("Test 1: Defaults")
    print("Create Transposition Cipher object (with defaults)")
    cipher = Transposition()

    print(plaintext)

    print('encrypt plaintext')
    ciphertext = cipher.encrypt(plaintext)
    print(ciphertext)

    print("Test 2: Custom number of rails (4)")
    custom_num_rails = 4
    print("Create Transposition Cipher object")
    cipher = Transposition(num_rails=4)

    print(plaintext)

    print('encrypt plaintext')
    ciphertext = cipher.encrypt(plaintext)
    print(ciphertext)

    print("Test 3: custom grouping (4)")
    custom_grouping = 4
    print("Create Transposition Cipher object")
    cipher = Transposition(grouping=custom_grouping)

    print(plaintext)

    print('encrypt plaintext')
    ciphertext = cipher.encrypt(plaintext)
    print(ciphertext)

    print("Test 4: custom grouping (no grouping)")
    custom_grouping = 0
    print("Create Transposition Cipher object")
    cipher = Transposition(grouping=custom_grouping)

    print(plaintext)

    print('encrypt plaintext')
    ciphertext = cipher.encrypt(plaintext)
    print(ciphertext)
