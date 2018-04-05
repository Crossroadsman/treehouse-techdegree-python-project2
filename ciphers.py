def rail_fence(plaintext, num_rails=3, grouping=5, strip_punctuation=True):
    '''Cipher where plaintext is written down and up the 'rails' of an
       imaginary fence.
       See <https://en.wikipedia.org/wiki/Transposition_cipher#Rail_Fence_cipher>
       for detailed description of the algorithm and example.
       This implementation accepts the following arguments:
       num_rails (default=3) : the number of fence rails
       grouping  (default=5) : the number of characters in a group (0 to not
                               break up into groups)
       strip_punctuation (default=True) : whether to encode just letters
                               and numbers or whether to encode all
                               characters (except spaces)
    '''
    
    STRIPPED_CHARACTERS = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
                           '0','1','2','3','4','5','6','7','8','9']
    
    rails = []
    
    # Optionally strip punctuation
    if strip_punctuation:
        plaintext = [c for c in plaintext if c.lower() in STRIPPED_CHARACTERS]
    else: # just strip spaces
        plaintext = [c for c in plaintext if c.lower() != " "]

        
    # Initialise rails
    for i in range(num_rails):
        rail = []
        for j in range(len(plaintext)):
            rail.append("")
        rails.append(rail)

    # Encode plaintext
    rail_number = 0
    down = True
    for i in range(len(plaintext)):
        #print("index: {}, character: {}, rail: {}".format(i, plaintext[i], rail_number))
        rails[rail_number][i] = plaintext[i]
        if down:
            # check if at bottom rail, if so switch to up
            if rail_number == num_rails -1:
                down = False
                rail_number -= 1
            else:
                rail_number += 1
        else:
            # check if at top rail, if so switch to down
            if rail_number == 0:
                down = True
                rail_number += 1
            else:
                rail_number -= 1
        
    # Flatten text
    ciphertext = ""
    for rail in rails:
        rail = "".join(rail)
        ciphertext += rail
    
    # Group characters
    if grouping > 0:
        grouped = ""
        for i in range(0, len(ciphertext)):
            if i % grouping == 0 and i != 0:
               grouped += " "
            grouped += ciphertext[i]
        ciphertext = grouped
    
    
    return ciphertext


def adfgvx(plaintext, keyphrase='PRIVACY', grouping=4):
    '''The ADFGVX cipher is a fractionating transposition cipher,
       combining a Polybius square with a single columnar transposition.
       For more discussion of the algorithm see:
       <https://en.wikipedia.org/wiki/ADFGVX_cipher>
       This implementation has two parameters:
       `plaintext` (str): the text to encode. Valid characters are 
                          letters (a-z, case insensitive) and
                          numbers (0-9).
    '''
    
    # Remove any invalid characters
    # -----------------------------
    # TBD

    # Polybius Square
    # ---------------

    POLYBIUS_SQUARE = {
        'a': {'a':'n', 'd':'a', 'f':'1', 'g':'c', 'v':'3', 'x':'h'},
        'd': {'a':'8', 'd':'t', 'f':'b', 'g':'2', 'v':'o', 'x':'m'},
        'f': {'a':'e', 'd':'5', 'f':'w', 'g':'r', 'v':'p', 'x':'d'},
        'g': {'a':'4', 'd':'f', 'f':'6', 'g':'g', 'v':'7', 'x':'i'},
        'v': {'a':'9', 'd':'j', 'f':'0', 'g':'k', 'v':'l', 'x':'q'},
        'x': {'a':'s', 'd':'u', 'f':'v', 'g':'x', 'v':'y', 'x':'z'},
    }
    
    def encode_character(x):
        '''takes a single character string and looks for it in the
           POLYBIUS_SQUARE. 
           returns a tuple of (row, col) if found.
           If not found, returns None (a separate dedicated function will 
           clean strings so that only valid characters will be passed into
           this function)
        '''
        for row, r_val in POLYBIUS_SQUARE.items():
            for col, c_val in r_val.items():
                if x == c_val:
                    return (row, col)
        return None
    
    for character in 'attack at 1200 am':
        print(encode_character(character), end='')
    print("")

    def decode_character(row,col):
        '''takes a pair of characters that correspond to a lookup
           reference in POLYBIUS_SQUARE.
           e.g., row='a', col='v' would return '3'
        '''
        return POLYBIUS_SQUARE[row][col]

    for pair in [('a','d'),('d','d'),('d','d'),('a','d'),('a','g'),('v','g')]:
        print(decode_character(*pair), end='')
    print("")

    # make columns using the keyword/phrase
    columns = []
    keyphrase_no_duplicates = []
    for character in keyphrase:
         if character not in keyphrase_no_duplicates:
             keyphrase_no_duplicates.append(character)

    for character in keyphrase_no_duplicates:
        # note that strings are effectively lists in Python so we don't
        # strictly need to explicitly put our characters into a list
        # but this approach makes our intent more explicit (especially
        # if being read by someone more familiar with languages (e.g., 
        # Swift) where strings are not simply glorified arrays
        columns.append([character.upper()])
    
    i = 0
    for character in plaintext:
        (row, col)  = encode_character(character)
        columns[i].append(row.lower())
        i = (i + 1) % len(keyphrase_no_duplicates)
        columns[i].append(col.lower())
        i = (i + 1) % len(keyphrase_no_duplicates)
        

    # sort the columns alphabetically
    columns = columns.sort()

    # take the letters from the columns and create a single long string
    ciphertext = ""
    for column in columns:
        for character in column[1:]:
            ciphertext.append(character)

    # break the string into blocks
    # TBD
    return ciphertext












# ------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    
    print("RAIL FENCE CIPHER EXAMPLES:")
    sample_text = "WE ARE DISCOVERED. FLEE AT ONCE"
    
    default = rail_fence(sample_text)
    print(default)

    four_rails = rail_fence(plaintext=sample_text,
                            num_rails=4)
    print(four_rails)

    groups_of_three = rail_fence(plaintext=sample_text,
                                 grouping=3)
    print(groups_of_three)

    ungrouped = rail_fence(plaintext=sample_text,
                           grouping=0)
    print(ungrouped)
 
    with_punc = rail_fence(plaintext=sample_text,
                           strip_punctuation=False)
    print(with_punc)
   

    print("ADFGVX CIPHER EXAMPLES")
    sample_text = "attack at 1200am"
    
    default = adfgvx(sample_text)
    print(sample_text)
