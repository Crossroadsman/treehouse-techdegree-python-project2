def rail_fence(plaintext, num_rails=3, grouping=5, strip_punctuation=True):
    '''Description of cipher goes here
    '''
    
    STRIPPED_CHARACTERS = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
                           '0','1','2','3','4','5','6','7','8','9']
    
    rails = []
    
    # Optionally strip punctuation
    if strip_punctuation:
        plaintext = [c for c in plaintext if c.lower() in STRIPPED_CHARACTERS]

        
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
        print("index: {}, character: {}, rail: {}".format(i, plaintext[i], rail_number))
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
        for i in range(1, len(ciphertext)):
            if i % grouping == 0:
               grouped += " "
            grouped += ciphertext[i]
        ciphertext = grouped
    
    
    print(ciphertext)
    return ciphertext
