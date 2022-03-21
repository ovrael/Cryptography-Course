# -----------------------------------------------------------
# Simple university project for cryptography course
# Demonstrates how to decrypt encrypted text without known key
#
# (C) 2022 Jacek Jendrzejewski, Poland
# -----------------------------------------------------------
def encryptCaesar(text: str,key: int):
    """Encrypt text to ceasar cipher by given key.

    Keyword arguments:\n
    string text -- text to encrypt\n
    int key -- key to shift letters\n
    returns string result -- ecrypted text
    """
    
    result = ""
    for i in range(len(text)):
        char = text[i].lower()
             
        # Skip space character
        if(char.isspace()):
            result += ' '
            continue

        # Encrypt lowercase characters in plain text
        else:
           result += chr((ord(char) + key - 97) % 26 + 97)
    return result

def decryptCaesarWithoutKey(encryptedText: str):
    """Decrypt encrypted text without given key

    Keyword arguments:\n
    string encryptedText -- text to decrypt\n
    returns void
    """
    
    # repeat decrypting proccess for every possible key
    for key in range(26):
        result = ""
        for i in range(len(encryptedText)):
            char = encryptedText[i].lower()
            
            # Skip space character
            if(char.isspace()):
                result += ' '
                continue
            
            # decrypt character and add to result text
            result += chr((ord(char) + key - 97) % 26 + 97)

        print(f"Key:{key}\nDecrypted text:{result}", end="\n\n")


text = input("Write encrypted text (e.g. 'rjytid n yjhmsnpn pwduytlwfknn' -> 'metody i techniki kryptografii' for key = 5):")

decryptCaesarWithoutKey(text)