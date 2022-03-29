### Symmetric cipher

from cryptography.fernet import Fernet
key = Fernet.generate_key()
f = Fernet(key)
encryptedMessage = f.encrypt(b"My deep dark secret")
print(encryptedMessage)
decryptedMessage = f.decrypt(encryptedMessage)
print(decryptedMessage)

### Asymmetric sipher

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.hashes import SHA256

# Private key
privateKey = rsa.generate_private_key(public_exponent=65537, key_size=2048)

privatePEM = privateKey.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)
print(f"Private key: {privatePEM}")

# Public key
publicPEM = privateKey.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format = serialization.PublicFormat.SubjectPublicKeyInfo
)

print(f"Public key: {publicPEM}")

### Encrypt and decrypt
privateKey = rsa.generate_private_key(public_exponent=65537, key_size=2048)
publicKey = privateKey.public_key()
clearText = "Ala ma kota".encode('utf-8')

for i in range(2):
    cipherText = publicKey.encrypt(
        clearText, padding.OAEP(
            mgf = padding.MGF1(algorithm=SHA256()),
            algorithm=SHA256(),
            label=None
        )
    )
    print(f"{i}-iteration cipher text: {cipherText.hex()}")


