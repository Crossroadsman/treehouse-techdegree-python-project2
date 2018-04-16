import string

from ciphers import Cipher


class Caesar(Cipher):
    FORWARD = string.ascii_uppercase * 3

    def __init__(self, offset=3, grouping=5):
        self.offset = offset
        self.FORWARD = string.ascii_uppercase + string.ascii_uppercase[:self.offset+1]
        self.BACKWARD = string.ascii_uppercase[:self.offset+1] + string.ascii_uppercase
        self.grouping = grouping
        if self.grouping != 0:
            self.PASSTHROUGH_CHARACTERS = []

    def encrypt(self, text):
        # reduce plaintext to valid characters
        if self.grouping != 0:
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
        self.PASSTHROUGH_CHARACTERS = []
        text = self._ungroup_text(text)
        text = text.upper()
        for char in text:
            try:
                index = self.BACKWARD.index(char)
            except ValueError:
                output.append(char)
            else:
                output.append(self.BACKWARD[index-self.offset])
        return ''.join(output)
