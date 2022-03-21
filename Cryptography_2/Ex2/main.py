# -----------------------------------------------------------
# Simple university project for cryptography course
# Demonstrates hashing features
#
# (C) 2022 Jacek Jendrzejewski, Poland
# -----------------------------------------------------------

import hashlib
import urllib.request

# 2. Ściągnij duży plik (np. ubuntu) i sprawdź, czy hash się zgadza.
# FILE: ubuntu-20.04.4-desktop-amd64
# SHA256 HASH: f92f7dca5bb6690e1af0052687ead49376281c7b64fbe4179cc44025965b7d1c

originalHash = 'f92f7dca5bb6690e1af0052687ead49376281c7b64fbe4179cc44025965b7d1c'
filePath = "https://releases.ubuntu.com/20.04/ubuntu-20.04.4-desktop-amd64.iso";

hasher = hashlib.sha256();

print("Hashing file from: " + filePath)
with urllib.request.urlopen(filePath) as fileData:
        data_chunk = fileData.read(1024)
        while data_chunk:
            hasher.update(data_chunk)
            data_chunk = fileData.read(1024)
              
print("Hashing ended")
hashedDownloadedFile = hasher.hexdigest()

if(hashedDownloadedFile == originalHash):
    print("HASH SUMS ARE EQUAL!")
else:
    print("HASH SUMS ARE NOT EQUAL")