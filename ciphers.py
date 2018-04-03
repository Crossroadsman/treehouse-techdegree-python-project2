def rail_fence(plaintext, num_rails=3):
    '''Description of cipher goes here
    '''
    
    rails = []
    
    # Initialise rails
    for i in range(num_rails):
        rail = []
        for j in range(len(plaintext)):
            rail.append("")
        rails.append(rail)

    # Encode plaintext
    rail_number = 0
    for i in range(len(plaintext)):
        print("index: {}, character: {}, rail: {}".format(i, plaintext[i], rail_number))
        rails[rail_number][i] = plaintext[i]
        rail_number = (rail_number + 1) % num_rails
        
    # Flatten text
    # TBD
    
    # Group characters
    # TBD
    
    for rail in rails:
        text = "".join(rail)
        print(text)
        
    return rails
