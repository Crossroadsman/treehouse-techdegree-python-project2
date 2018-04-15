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

    def _ungroup_text(self, text):
        '''Converts a string of groups into a single 'word'
        '''
        output = ""
        for character in text:
            if character != " ":
                output += character
        return output
    
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

    def _apply_one_time_pad(self, pad, plaintext, encrypt_mode=True):
        '''takes a valid one-time pad (array of ints, at least as long as the
        plaintext) and a plaintext and then returns a new 'plaintext' with the
        pad applied (forward if encrypting, backward if decrypting)
        '''
        altered_plaintext = ""
        numchars = len(plaintext)
        for character_index in range(numchars):
            character = plaintext[character_index].lower()
            lookup_index = self.VALID_CHARACTERS.index(character)
            if encrypt_mode:
                offset_index = (lookup_index + pad[character_index]) % numchars
            else:
                offset_index = (lookup_index - pad[character_index]) % numchars
            altered_plaintext += self.VALID_CHARACTERS[offset_index]
        return altered_plaintext
