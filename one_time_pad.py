class OneTimePad():

    def __init__(self, pad_numbers, plaintext):
        validated = self._validate_pad(pad_numbers, len(plaintext)):
        self.error = validated['error']
        self.pad_numbers = validated['pad_numbers']
    
    def _validate_pad(self, pad_numbers, min_length):
        '''takes a user-supplied prospective one-time pad and determines its
        validity.
        Returns a dictionary with two keys, `error` and `pad_numbers`.
        If the pad is valid, error will be None and pad_numbers will be the values
        (None can be a valid value for pad_numbers).
        If the pad is invalid, error will be a description of the error and
        pad_numbers will be None
        '''
        # check if pad is blank
        if pad_numbers == '':
            error = None
            pad_numbers = None
            return {'error': error,
                    'pad_numbers': pad_numbers}

        # turn comma-separated into list of values
        pad_numbers = pad_numbers.split(',')

        # try to convert the list elements into ints
        try:
            pad_numbers = [int(element) for element in pad_numbers]
        except ValueError:
            error = 'Invalid characters in pad, should only contain ints'
            pad_numbers = None
            return {'error': error,
                    'pad_numbers': pad_numbers}

        # check the length is sufficient
        if len(pad_numbers) < min_length:
            error = 'Too short, pad must be at least as long as plaintext'
            pad_numbers = None
        else:
            error = None
        return {'error': error,
                'pad_numbers': pad_numbers}
    
    def apply_one_time_pad(self, plaintext, cipher, encrypt_mode=True):
        '''reads the object's valid one-time pad (array of ints, at least as
        long as the plaintext) and takes:
        - plaintext (the text that will have the pad applied);
        - cipher (the cipher object - needed to use the cipher functionality);
        - encrypt_mode (True if encrypting, False if decrypting)
        and then returns a new 'plaintext' with the
        pad applied (forward if encrypting, backward if decrypting)
        '''
        valid_characters_and_spaces = cipher._reduce_characters(plaintext)
        altered_plaintext = ""
        numchars = len(valid_characters_and_spaces)
        numvalid = len(cipher.VALID_CHARACTERS)

        for character_index in range(numchars):
            character = valid_characters_and_spaces[character_index].lower()
            if character in cipher.VALID_CHARACTERS:
                lookup_index = cipher.VALID_CHARACTERS.index(character)
                if encrypt_mode:
                    offset_index = (lookup_index + self.pad_numbers[character_index]) % numvalid
                else:
                    offset_index = (lookup_index - self.pad_numbers[character_index]) % numvalid
                altered_plaintext += cipher.VALID_CHARACTERS[offset_index]
            elif character in cipher.PASSTHROUGH_CHARACTERS:
                altered_plaintext += character
                
        return altered_plaintext