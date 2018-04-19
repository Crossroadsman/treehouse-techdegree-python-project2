import string

from ciphers import Cipher


class Caesar(Cipher):
    UPPERCASE = string.ascii_uppercase
    FORWARD = UPPERCASE * 3

    def __init__(self, offset=3, grouping=5):
        self.offset = offset

        self.FORWARD = self.UPPERCASE + self.UPPERCASE[:self.offset+1]
        self.BACKWARD = self.UPPERCASE[:self.offset+1] + self.UPPERCASE
        self.grouping = grouping
        if self.grouping != 0:
            self.PASSTHROUGH_CHARACTERS = []
        else:
            self.PASSTHROUGH_CHARACTERS = [' ']

    def encrypt(self, text):
        # reduce plaintext to valid characters
        text = self._reduce_characters(text)

        output = []
        text = text.upper()
        for char in text:
            try:
                index = self.FORWARD.index(char)
            except ValueError:
                output.append(char)
            else:
                output.append(self.FORWARD[index+self.offset])
        enciphered = ''.join(output)
        grouped = self._group_text(enciphered)
        return grouped

    def decrypt(self, text):
        output = []
        if self.grouping != 0:
            print("grouping ({}) != 0".format(self.grouping))
            text = self._ungroup_text(text)
            print(text)

        text = text.upper()
        for char in text:
            try:
                index = self.BACKWARD.index(char)
            except ValueError:
                output.append(char)
            else:
                output.append(self.BACKWARD[index-self.offset])
        return ''.join(output)

# -------------------------------------------------------------

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
        'b: offset only (4)': {'offset': 4},
        'c: grouping only (none)': {'grouping': 0},
        'd: grouping only (3)': {'grouping': 3},
        'e: offset (4) and grouping (3)': {'offset': 4,
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
        run_tests(Caesar, plaintext, tests)
