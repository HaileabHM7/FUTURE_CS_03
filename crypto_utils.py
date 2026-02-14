import os
import hashlib

# Try this first
try:
    from Crypto.Cipher import AES
except ImportError:
    from Cryptodome.Cipher import AES

# Get the passphrase from environment variable
passphrase = os.environ.get("AES_PASSPHRASE")

if passphrase is None:
    # Prompt for passphrase if not in environment
    passphrase = input("Enter encryption passphrase: ")

# Hash the passphrase to get a 32-byte key
KEY = hashlib.sha256(passphrase.encode()).digest()  # Always 32 bytes

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