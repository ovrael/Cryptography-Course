import random


def split_len(sequence, length):  
   return [sequence[i:i + length] for i in range(0, len(sequence), length)]

def findPrimes(count):
    primes = []
    i = 1
    while len(primes) < count:
        if checkIfPrime(i):
            primes.append(i)
        i += 1
        
    return primes

def checkIfPrime(number):
    
    if number < 2:
        return False
    
    for i in range(2, int(number**0.5)+1):
        if (number % i) == 0:
            return False
    return True   

def createSubstitutes():
    primes = findPrimes(2*(ord('z')-ord('a')+1))
    substitutes = {}
    k = 0
    for i in range(ord('a'), ord('z')+1):
        substitutes[chr(i)] = ['{0:03}'.format(primes[k]),'{0:03}'.format(primes[len(primes)-1-k])]
        k +=1
    return substitutes
    
def encode(key, plainText): 
    
    indexes = key.split(',')
     
    order = {  
        int(val): n for n, val in enumerate(indexes)
    }
    
    substitutes = createSubstitutes()
    
    ciphertext = ''  
      
    for index in sorted(order.keys()):  
        for part in split_len(plainText, len(indexes)):  
            try:
                char = part[order[index]]
                            
                if char.isalpha():
                    char = char.lower()
                    char = substitutes[char][random.randint(0, len(substitutes[char]))]
                
                ciphertext += char
            except IndexError:  
                continue
            except Exception as e:
                print(f"-------------- ERROR: {e}")
                continue
    return ciphertext  


fileText = ''
with open('Cryptography_5\\text.txt') as plainTextFile:
    fileText = plainTextFile.read()

encodedText = encode('3,6,2,4,5,1,7', fileText)

with open('Cryptography_5\\encodedText.txt', "w") as encodedTextFile:
    encodedTextFile.write(encodedText)