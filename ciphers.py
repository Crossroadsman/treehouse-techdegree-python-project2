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

if __name__ == "__main__":

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
   
def adfgvx(plaintext, grouping=4):
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
        for row, r_val in POLYBIUS_SQUARE.items():
            for col, c_val in row.items():
                if x == c_val:
                    return (row, col)
        return None
    
    
