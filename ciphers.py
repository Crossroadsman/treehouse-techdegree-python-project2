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
        rails[rail_number][i] = plaintext[i]
        rail_number = (rail_number + 1) % num_rails
        
    # Flatten text
    # TBD
    
    # Group characters
    # TBD
    
    for rail in rails:
        for character in rail:
            print(character)
        
    return rails
    
    
