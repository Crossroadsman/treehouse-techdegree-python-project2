VALID_CIPHERS = {
    'c': 'Caesar', 
    't': 'Transposition', 
    'a': 'ADFGVX', 
    'p': 'Polybius Square', 
    'k': 'Keyword',
}
VALID_ACTIVITIES = {
    'e': 'encrypt',
    'd': 'decrypt',
}

print("This is the Secret Messages project for the Treehouse Techdegree\n")
print("These are the current available ciphers:\n")
for key, value in VALID_CIPHERS.items():
    shortcut = "[" + key.upper() + "]"
    remainder = value[1:].lower()
    print(shortcut + remainder)

cipher_choice = input("Which cipher would you like to use? ").lower()
while cipher_choice not in VALID_CIPHERS.keys():
    print("I'm sorry, I didn't recognise that choice. Please try again.")
    print("Valid choices are: ")
    for letter in VALID_CIPHERS.keys():
        print(letter)
    cipher_choice = input("Which cipher would you like to use? ").lower()

plaintext = input("That's an excellent cipher. What's the message? ")

process = input("Which process do you want to use? ")
for key, value in VALID_ACTIVITIES.items():
    shortcut = "[" + key.upper() + "]"
    remainder = value[1:].lower()
    print(shortcut + remainder)

while process not in VALID_ACTIVITIES.keys():
    print("I'm sorry, I didn't recognise that choice. Please try again.")
    print("Valid choices are: ")
    for letter in VALID_ACTIVITIES.keys():
        print(letter)
    process = input("Which process do you want to use? ")

pad_number = input('Please enter the pad number: ')



