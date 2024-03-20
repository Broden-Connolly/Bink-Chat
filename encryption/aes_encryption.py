from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

# Encrypt Data
data = b'secret data'
print (data)
key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(data)
nonce = cipher.nonce

print(ciphertext)

# Decrypt Data
cipher = AES.new(key, AES.MODE_EAX, nonce)
data = cipher.decrypt_and_verify(ciphertext, tag)

print(data)