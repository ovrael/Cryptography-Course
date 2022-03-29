##############################
#                            #
#  Jacek Jendrzejewski 2022  #
#                            #
##############################

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

# RUN -> python -m uvicorn main:[BELOW VARIABLE NAME] --reload
app = FastAPI()

### Symmetric key ###

# GET symmetric/key -> zwraca losowo wygenerowany klucz symetryczny w postaci HEXów (może być JSON)
@app.get("/symmetric/key")
async def createSymmetricKey():
    return {"key": "hexValues"}
    
# POST symmetric/key -> ustawia na serwerze klucz symetryczny podany w postaci HEX w request
@app.post("/symmetric/key")
async def setSymmetricKey(symmetricKey: str):
    return symmetricKey

# POST symmetric/encode -> wysyłamy wiadomość, w wyniku dostajemy ją zaszyfrowaną
@app.post("/symmetric/encode")
async def encodeMessageSymmetric(message: str):
    encodedMessage = f"Given message: {message} -> encoded: message"
    return encodedMessage

# POST symmetric/decode -> wysyłamy wiadomość, w wyniku dostajemy ją odszyfrowaną
@app.post("/symmetric/decode")
async def decodeMessageSymmetric(message: str):
    decodedMessage = f"Given message: {message} -> decoded: message"
    return decodedMessage


### Assymmetric key ###

# GET asymmetric/key -> zwraca nowy klucz publiczny i prywatny w postaci HEX (w JSON jako dict) i ustawia go na serwerze
@app.get("/asymmetric/key")
async def createAndSetAsymmetricKey():
    return {"key": "hexValues"}

# GET asymmetric/key/ssh -> zwraca klucz publiczny i prywatny w postaci HEX zapisany w formacie OpenSSH
@app.get("/asymmetric/key/ssh")
async def getAsymmetricKeyOpenSSH():
    return {"key": "hexValues"}

# POST asymmetric/key -> ustawia na serwerze klucz publiczny i prywatny w postaci HEX (w JSON jako dict)
@app.post("/asymmetric/key")
async def setAsymmetricKey(message: str):
    decodedMessage = f"Given message: {message} -> decoded: message"
    return decodedMessage

# POST asymmetric/sign -> korzystając z aktualnie ustawionego klucza prywatnego, podpisuje wiadomość i zwracaą ją podpisaną
@app.post("/asymmetric/sign")
async def signMessageWithAsymmetricKey(message: str):
    decodedMessage = f"Given message: {message} -> decoded: message"
    return decodedMessage

# POST asymmetric/verify -> korzystając z aktualnie ustawionego klucza publicznego, weryfikuję czy wiadomość była zaszyfrowana przy jego użyciu
@app.post("/symmetric/verify")
async def verifyMessageWithAsymmetricKey(message: str):
    decodedMessage = f"Given message: {message} -> decoded: message"
    return decodedMessage

# POST asymmetric/encode -> wysyłamy wiadomość, w wyniku dostajemy ją zaszyfrowaną
@app.post("/asymmetric/encode")
async def decodeMessageAsymmetric(message: str):
    decodedMessage = f"Given message: {message} -> decoded: message"
    return decodedMessage

# POST asymmetric/decode -> wysyłamy wiadomość, w wyniku dostajemy ją odszyfrowaną
@app.post("/asymmetric/decode")
async def decodeMessageAsymmetric(message: str):
    decodedMessage = f"Given message: {message} -> decoded: message"
    return decodedMessage