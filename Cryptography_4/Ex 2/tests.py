from cryptography.fernet import Fernet
import binascii
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.hashes import SHA256


# key = Fernet.generate_key()
# key = binascii.hexlify(key)
# key = binascii.unhexlify(key)
# f = Fernet(key)
# encryptedMessage = f.encrypt(b'My deep dark secret')
# print(encryptedMessage)
# decryptedMessage = f.decrypt(encryptedMessage)
# print(decryptedMessage)

privateKey = rsa.generate_private_key(public_exponent=65537, key_size=2048)
publicKey = binascii.hexlify(privateKey.public_key())
publicKey = binascii.unhexlify(publicKey)


clearText = "Ala ma kota".encode('utf-8')

cipherText = publicKey.encrypt(
        clearText, padding.OAEP(
            mgf = padding.MGF1(algorithm=SHA256()),
            algorithm=SHA256(),
            label=None
        )
    )

print(cipherText)