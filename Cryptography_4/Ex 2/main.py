##############################
#                            #
#  Jacek Jendrzejewski 2022  #
#                            #
##############################

### API IMPORTS
import base64
import hashlib
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
from cryptography.hazmat.backends import default_backend
import cryptography.exceptions

# Imports
import binascii

### KEYS
class Symmetric(BaseModel):
    key: str = None
    
class Asymmetric(BaseModel):
    privateKey: str = None
    publicKey: str = None
    
# RUN -> python -m uvicorn main:[BELOW VARIABLE NAME] --reload
app = FastAPI()
symmetric = Symmetric()
asymmetric = Asymmetric()

### Symmetric key ###

# GET symmetric/key -> zwraca losowo wygenerowany klucz symetryczny w postaci HEXów (może być JSON)
@app.get("/symmetric/key")
async def create_symmetric_key():
    """Creates symmetric key by using Fernet

    Parameters:
        None

    Returns:
        symmetric key in HEX format in JSON
    """
    key = Fernet.generate_key()
    key = binascii.hexlify(key)
    return {"symmetricKey": key}
    
# POST symmetric/key -> ustawia na serwerze klucz symetryczny podany w postaci HEX w request
@app.post("/symmetric/key")
async def set_symmetricKey(symmetricKeyHex: str):
    """Sets symmetric key in HEX format

    Parameters:
        symmetricKeyHex (str): symmetric key in HEX format

    Returns:
        Information about successfully set key
    """
    symmetric.key = symmetricKeyHex
    return "Symmetric key is set."

# POST symmetric/encode -> wysyłamy wiadomość, w wyniku dostajemy ją zaszyfrowaną
@app.post("/symmetric/encode")
async def encode_message_symmetric(message: str):
    """Uses symmetric key to encrypts message

    Parameters:
        message (str): plain message to be ecnrypted

    Returns:
        Encrypted message or information about occured error.
    """
    
    if  symmetric.key is None:
        return "Symmetric key is None!"
    
    try:
        key = binascii.unhexlify(symmetric.key)
        fernetObject = Fernet(key)
        encodedMessage = fernetObject.encrypt(message.encode())
    except Exception as e:
        return f"Sorry, following error occured: {e}."
    
    return encodedMessage

# POST symmetric/decode -> wysyłamy wiadomość, w wyniku dostajemy ją odszyfrowaną
@app.post("/symmetric/decode")
async def decode_message_symmetric(message: str):
    """Uses symmetric key to decrypts message

    Parameters:
        message (str): encrypted message to be decrypted

    Returns:
        Decrypted message or information about occured error.
    """

    if  symmetric.key is None:
        return "Symmetric key is None!"
    
    try:
        key = binascii.unhexlify(symmetric.key)
        fernetObject = Fernet(key)
        decryptedMessage = fernetObject.decrypt(message.encode())
    except Exception as e:
        return f"Sorry, following error occured: {e}."
    
    return decryptedMessage


### Assymmetric key ###

# GET asymmetric/key -> zwraca nowy klucz publiczny i prywatny w postaci HEX (w JSON jako dict) i ustawia go na serwerze
@app.get("/asymmetric/key")
async def create_and_set_asymmetric_key():
    """Creates asymmetric private and public keys and sets them on the server

    Parameters:
        None

    Returns:
        asymmetric keys in HEX format in JSON dictionary or information about occured error
    """
    privateKey = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    
    try:
        privatePEM = privateKey.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        publicPEM = privateKey.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format = serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        asymmetric.privateKey = privatePEM.hex()
        asymmetric.publicKey = publicPEM.hex()
        
    except Exception as e:
        return f"Sorry, following error occured: {e}."
    
    return { "privateKey": asymmetric.privateKey, "publicKey": asymmetric.publicKey}

# GET asymmetric/key/ssh -> zwraca klucz publiczny i prywatny w postaci HEX zapisany w formacie OpenSSH
@app.get("/asymmetric/key/ssh")
async def get_asymmetric_key_openSSH():
    """Gets asymmetric keys that are set on the server

    Parameters:
        None

    Returns:
        asymmetric keys
    """
    return { "privateKey": asymmetric.privateKey, "publicKey": asymmetric.publicKey}

# POST asymmetric/key -> ustawia na serwerze klucz publiczny i prywatny w postaci HEX (w JSON jako dict)
@app.post("/asymmetric/key")
async def set_asymmetric_key(keys: Asymmetric):
    """Sets asymmetric keys on the server

    Parameters:
        keys (Asymmetric): asymmetric keys object with both keys

    Returns:
        information about set keys
    """

    asymmetric.privateKey = keys.privateKey
    asymmetric.publicKey = keys.publicKey

    return "Asymmetric keys are set!"

# POST asymmetric/sign -> korzystając z aktualnie ustawionego klucza prywatnego, podpisuje wiadomość i zwracaą ją podpisaną
@app.post("/asymmetric/sign")
async def sign_message(message: str):
    """Uses asymmetric private key to sign the message

    Parameters:
        message (str): plain message to be signed

    Returns:
        Signed signature of message
    """
    if  asymmetric.privateKey is None:
        return "Asymmetric private key is None!"
    
    try:
        key = bytes.fromhex(asymmetric.privateKey)
        
        privateKey = serialization.load_pem_private_key(
            key,
            password=None,
            backend=default_backend()
        )
        
        hashedMessage = hashlib.sha256(message.encode('utf-8')).hexdigest()
        signature = privateKey.sign(
            bytes(hashedMessage.encode('ascii')),
            padding.PSS( mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return base64.b64encode(signature)
    except Exception as e:
        return f"Sorry, following error occured: {e}."


# POST asymmetric/verify -> korzystając z aktualnie ustawionego klucza publicznego, weryfikuję czy wiadomość była zaszyfrowana przy jego użyciu
@app.post("/symmetric/verify")
async def verify_message(message: str, signature: str):
    """Uses asymmetric public key to verify whether message is signed by currently set key

    Parameters:
        message (str): plain message that was signed
        signature (str): signed message

    Returns:
        information if provided message is signed by currently set key or information about occured error
    """
    if(asymmetric.publicKey is None):
        return "Asymmetric public key is None!"
    
    try:     
        key = bytes.fromhex(asymmetric.publicKey)
        publicKey = serialization.load_pem_public_key(
            key,
            backend=default_backend()
        )
        
        hashedMessage = hashlib.sha256(message.encode('utf-8')).hexdigest()

        publicKey.verify(
            base64.b64decode(signature),
            bytes(hashedMessage.encode('ascii')),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        pass
    except cryptography.exceptions.InvalidSignature as e:
        return "Message is not signed with currently set public key!"
    except Exception as e:
        return f"Sorry, following error occured: {e}."
    
    return "Message is signed and verified with currently set public key!"


# POST asymmetric/encode -> wysyłamy wiadomość, w wyniku dostajemy ją zaszyfrowaną
@app.post("/asymmetric/encode")
async def encode_message_asymmetric(message: str):
    """Uses asymmetric public key to encrypt the message

    Parameters:
        message (str): plain message to be encrypted

    Returns:
        encrypted message or information about occured error
    """
    if(asymmetric.publicKey is None):
        return "Asymmetric public key is None!"
    
    try:
        key = bytes.fromhex(asymmetric.publicKey)
        publicKey = serialization.load_pem_public_key(
            key,
            backend=default_backend()
        )
            
        encryptedMessage = publicKey.encrypt(
            base64.b64encode(bytes(message, 'ascii')),
            padding.OAEP(
                mgf = padding.MGF1(algorithm=SHA256()),
                algorithm=SHA256(),
                label=None
            )
        )
        return base64.b64encode(encryptedMessage)
    except Exception as e:
        return f"Sorry, following error occured: {e}."

# POST asymmetric/decode -> wysyłamy wiadomość, w wyniku dostajemy ją odszyfrowaną
@app.post("/asymmetric/decode")
async def decode_message_asymmetric(message: str):
    """Uses asymmetric private key to decrypt the message

    **Parameters**:
        message (str): encrypted message to be decrypted

    Returns:
        decrypted message or information about occured error
    """
    if(asymmetric.publicKey is None):
        return "Asymmetric public key is None!"
    
    try:
        key = bytes.fromhex(asymmetric.privateKey)
        
        privateKey = serialization.load_pem_private_key(
            key,
            password=None,
            backend=default_backend()
        )
        
        decryptedMessage = privateKey.decrypt(
            base64.b64decode(message),
            padding.OAEP(
                mgf = padding.MGF1(algorithm=SHA256()),
                algorithm=SHA256(),
                label=None
            )
        )
        return base64.b64decode(decryptedMessage)
    except Exception as e:
        return f"Sorry, following error occured: {e}."
