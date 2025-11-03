# encryption.py
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os

# --- Configuration ---
KEY_SIZE = 32  # 256-bit key
SALT_SIZE = 16 # 128-bit salt
PBKDF2_ITERATIONS = 100000 # Number of iterations for key derivation

def get_key_from_password(password, salt):
    """Derives a 256-bit key from a password and salt using PBKDF2."""
    return PBKDF2(password, salt, dkLen=KEY_SIZE, count=PBKDF2_ITERATIONS)

def encrypt_text(text, password):
    """
    Encrypts a string using a key derived from the password.
    Returns the salt and the encrypted text.
    """
    salt = get_random_bytes(SALT_SIZE)
    key = get_key_from_password(password.encode('utf-8'), salt)

    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv

    encrypted_data = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))

    # Return a single blob: salt + iv + ciphertext
    return salt + iv + encrypted_data

def decrypt_text(encrypted_blob, password):
    """
    Decrypts a blob of encrypted data using a key derived from the password.
    """
    try:
        salt = encrypted_blob[:SALT_SIZE]
        iv = encrypted_blob[SALT_SIZE:SALT_SIZE + 16]
        ciphertext = encrypted_blob[SALT_SIZE + 16:]

        key = get_key_from_password(password.encode('utf-8'), salt)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted_data.decode('utf-8')
    except (ValueError, KeyError, IndexError):
        # Errors can occur from incorrect password, corrupted data, or invalid format
        return None

def encrypt_file(input_path, output_path, password):
    """
    Encrypts a file using a password-derived key.
    """
    salt = get_random_bytes(SALT_SIZE)
    key = get_key_from_password(password.encode('utf-8'), salt)

    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv

    with open(input_path, 'rb') as f_in:
        plaintext = f_in.read()

    encrypted_data = cipher.encrypt(pad(plaintext, AES.block_size))

    with open(output_path, 'wb') as f_out:
        f_out.write(salt)
        f_out.write(iv)
        f_out.write(encrypted_data)

def decrypt_file(input_path, output_path, password):
    """
    Decrypts a file using a password-derived key.
    Returns True on success, False on failure.
    """
    try:
        with open(input_path, 'rb') as f_in:
            salt = f_in.read(SALT_SIZE)
            iv = f_in.read(16)
            ciphertext = f_in.read()

        key = get_key_from_password(password.encode('utf-8'), salt)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)

        with open(output_path, 'wb') as f_out:
            f_out.write(decrypted_data)

        return True
    except (ValueError, KeyError, FileNotFoundError):
        return False
