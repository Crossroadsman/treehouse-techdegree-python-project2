class Cipher:

    VALID_CHARACTERS = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    def encrypt(self):
        raise NotImplementedError()

    def decrypt(self):
        raise NotImplementedError()

    def _reduce_characters(self, text):
        reduced_text = ""
        for character in text:
            if character.lower() in self.VALID_CHARACTERS:
                reduced_text += character
        return reduced_text
