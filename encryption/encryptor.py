import os
import base64
from cryptography.fernet import Fernet

# Path to key file
KEY_FILE = "encryption_key.key"

# Load or generate encryption key
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, 'rb') as f:
        key = f.read()
else:
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)

# Initialize cipher using the loaded key
cipher = Fernet(key)

def encrypt_message(message: str) -> str:
    """
    Encrypts a string and returns a base64-encoded string.
    """
    encrypted_bytes = cipher.encrypt(message.encode())
    return base64.urlsafe_b64encode(encrypted_bytes).decode()

def decrypt_message(encoded_str: str) -> str:
    """
    Decrypts a base64-encoded string and returns the original message.
    """
    encrypted_bytes = base64.urlsafe_b64decode(encoded_str.encode())
    return cipher.decrypt(encrypted_bytes).decode()
