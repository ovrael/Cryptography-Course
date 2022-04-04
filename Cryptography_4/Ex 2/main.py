##############################
#                            #
#  Jacek Jendrzejewski 2022  #
#                            #
##############################

### API IMPORTS
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

### KEYS IMPORTS
from cryptography.fernet import Fernet

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.hashes import SHA256
import cryptography.exceptions

# Imports
import binascii

### KEYS
class SymmetricKey(BaseModel):
    key: str = None
    
class AsymmetricKeys(BaseModel):
    private: str = None
    public: str = None

# RUN -> python -m uvicorn main:[BELOW VARIABLE NAME] --reload
app = FastAPI()
symmetricKey = SymmetricKey()
asymmetricKeys = AsymmetricKeys()

### Symmetric key ###

# GET symmetric/key -> zwraca losowo wygenerowany klucz symetryczny w postaci HEXów (może być JSON)
@app.get("/symmetric/key")
async def createSymmetricKey():
    key = Fernet.generate_key()
    key = binascii.hexlify(key)
    return {"symmetricKey": key}
    
# POST symmetric/key -> ustawia na serwerze klucz symetryczny podany w postaci HEX w request
@app.post("/symmetric/key")
async def setSymmetricKey(symmetricKeyHex: str):
    symmetricKey.key = symmetricKeyHex
    return "Symmetric key is set."

# POST symmetric/encode -> wysyłamy wiadomość, w wyniku dostajemy ją zaszyfrowaną
@app.post("/symmetric/encode")
async def encodeMessageSymmetric(message: str):
    if  symmetricKey.key is None:
        return "Symmetric key is None!"
    
    key = binascii.unhexlify(symmetricKey.key)
    fernetObject = Fernet(key)
    encodedMessage = fernetObject.encrypt(message.encode())
    return encodedMessage

# POST symmetric/decode -> wysyłamy wiadomość, w wyniku dostajemy ją odszyfrowaną
@app.post("/symmetric/decode")
async def decodeMessageSymmetric(message: str):
    if  symmetricKey.key is None:
        return "Symmetric key is None!"
        
    key = binascii.unhexlify(symmetricKey.key)
    fernetObject = Fernet(key)
    decryptedMessage = fernetObject.decrypt(message.encode())
    return decryptedMessage


### Assymmetric key ###

# GET asymmetric/key -> zwraca nowy klucz publiczny i prywatny w postaci HEX (w JSON jako dict) i ustawia go na serwerze
@app.get("/asymmetric/key")
async def createAndSetAsymmetricKey():
    privateKey = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        
    # privatePEM = privateKey.private_bytes(
    #     encoding=serialization.Encoding.PEM,
    #     format=serialization.PrivateFormat.OpenSSH,
    #     encryption_algorithm=serialization.NoEncryption()
    # )
    
    # publicPEM = privateKey.public_key().public_bytes(
    #     encoding=serialization.Encoding.PEM,
    #     format = serialization.PublicFormat.OpenSSH
    # )
    
    asymmetricKeys.private = privateKey
    asymmetricKeys.public = privateKey.public_key()
    
    privateKey.sign()

    return {"privateKey": asymmetricKeys.private, "publicKey" : asymmetricKeys.public}

# GET asymmetric/key/ssh -> zwraca klucz publiczny i prywatny w postaci HEX zapisany w formacie OpenSSH
@app.get("/asymmetric/key/ssh")
async def getAsymmetricKeyOpenSSH():
    return {"privateKey": asymmetricKeys.private, "publicKey" : asymmetricKeys.public}

# POST asymmetric/key -> ustawia na serwerze klucz publiczny i prywatny w postaci HEX (w JSON jako dict)
@app.post("/asymmetric/key")
async def setAsymmetricKey(keys: AsymmetricKeys):

    asymmetricKeys.private = keys["private"]
    asymmetricKeys.public = keys["public"]

    return "Asymmetric keys are set!"

# POST asymmetric/sign -> korzystając z aktualnie ustawionego klucza prywatnego, podpisuje wiadomość i zwracaą ją podpisaną
@app.post("/asymmetric/sign")
async def signMessageWithAsymmetricKey(message: str):
    if  asymmetricKeys.private is None:
        return "Asymmetric private key is None!"
    
    signature = asymmetricKeys.private.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
        
    return signature

# POST asymmetric/verify -> korzystając z aktualnie ustawionego klucza publicznego, weryfikuję czy wiadomość była zaszyfrowana przy jego użyciu
@app.post("/symmetric/verify")
async def verifyMessageWithAsymmetricKey(message: str, signature: str):
    if(asymmetricKeys.public is None):
        return "Asymmetric public key is None!"
    
    verified = True
    try:
        asymmetricKeys.public.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        pass
    except cryptography.exceptions.InvalidSignature as e:
        verified = False
    
    return verified

# POST asymmetric/encode -> wysyłamy wiadomość, w wyniku dostajemy ją zaszyfrowaną
@app.post("/asymmetric/encode")
async def encodeMessageAsymmetric(message: str):
    if(asymmetricKeys.public is None):
        return "Asymmetric public key is None!"
    
    encodedMessage = asymmetricKeys.public.encrypt(
        message.encode('utf-8'), padding.OAEP(
            mgf = padding.MGF1(algorithm=SHA256()),
            algorithm=SHA256(),
            label=None
        )
    )
    return encodedMessage

# POST asymmetric/decode -> wysyłamy wiadomość, w wyniku dostajemy ją odszyfrowaną
@app.post("/asymmetric/decode")
async def decodeMessageAsymmetric(message: str):
    if(asymmetricKeys.public is None):
        return "Asymmetric public key is None!"
    
    decodedMessage = asymmetricKeys.private.decrypt(
        message, padding.OAEP(
            mgf = padding.MGF1(algorithm=SHA256()),
            algorithm=SHA256(),
            label=None
        )
    )
    return decodedMessage.decode('utf-8')