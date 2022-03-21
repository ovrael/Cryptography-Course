# -----------------------------------------------------------
# Simple university project for cryptography course
# Demonstrates hashing features
#
# (C) 2022 Jacek Jendrzejewski, Poland
# -----------------------------------------------------------

# 1. Zaimplementuj hashowanie wszystkimi funkcjami zwracanymi przez algorithms_available z biblioteki hashlib wraz ze zwróceniem informacji o czasie hashowania dla danych wejściowych z konsoli.
import hashlib
import time
availableHashFunctions = hashlib.algorithms_available

text = input("Write text to hash by available algorithms in hashlib library:")

for algorithmName in availableHashFunctions:
    
    start = time.perf_counter()
    
    try:
        hasher = hashlib.new(algorithmName)
        hasher.update(text.encode())
        hashedText = hasher.hexdigest()
        
    except TypeError:        
        hashedText = hasher.hexdigest(32)
    except Exception as e:
        print(f"------- An exception: {e} occurred with {algorithmName}", end="\n\n")
        continue
    
    stop = time.perf_counter()
    elapsedSeconds = stop - start
    print(f"Algorigthm: {algorithmName}\nHashed text: {hashedText} \nTake {elapsedSeconds} seconds", end="\n\n")