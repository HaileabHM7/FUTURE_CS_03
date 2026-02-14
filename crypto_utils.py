import os
import hashlib

try:
    from Crypto.Cipher import AES
except ImportError:
    from Cryptodome.Cipher import AES

passphrase = os.environ.get("AES_PASSPHRASE")

if passphrase is None:
    passphrase = input("Enter encryption passphrase: ")

KEY = hashlib.sha256(passphrase.encode()).digest()  

def encrypt_file(data):
    cipher = AES.new(KEY, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce + tag + ciphertext

def decrypt_file(data):
    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]
    cipher = AES.new(KEY, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)