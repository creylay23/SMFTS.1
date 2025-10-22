from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import hashlib
import os

# AES key length in bytes (256 bits)
KEY_LENGTH = 32

def generate_key():
    """Generates a secure 256-bit (32-byte) key."""
    return get_random_bytes(KEY_LENGTH)

def encrypt_file(input_path, output_path, key):
    """Encrypts a file using AES-256 in CBC mode."""
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv

    with open(input_path, 'rb') as f_in:
        plaintext = f_in.read()

    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    with open(output_path, 'wb') as f_out:
        f_out.write(iv)
        f_out.write(ciphertext)

def decrypt_file(input_path, output_path, key):
    """Decrypts a file encrypted with AES-256 in CBC mode."""
    with open(input_path, 'rb') as f_in:
        iv = f_in.read(16)
        ciphertext = f_in.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)

    try:
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        with open(output_path, 'wb') as f_out:
            f_out.write(plaintext)
        return True
    except (ValueError, KeyError):
        # This occurs if the key is incorrect or data is corrupted
        return False

def encrypt_message(message, key):
    """Encrypts a text message using AES-256."""
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv

    padded_message = pad(message.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_message)

    return iv + ciphertext

def decrypt_message(ciphertext, key):
    """Decrypts an AES-256 encrypted message."""
    iv = ciphertext[:16]
    encrypted_message = ciphertext[16:]

    cipher = AES.new(key, AES.MODE_CBC, iv)

    try:
        decrypted_message = unpad(cipher.decrypt(encrypted_message), AES.block_size)
        return decrypted_message.decode('utf-8')
    except (ValueError, KeyError):
        return None # Decryption failed

def get_file_hash(filepath):
    """Calculates the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        # Read the file in chunks to handle large files
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()
