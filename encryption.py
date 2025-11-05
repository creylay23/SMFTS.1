from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import hashlib
import os

# --- Path Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYS_DIR = os.path.join(BASE_DIR, "keys")

# AES key length in bytes (256 bits)
KEY_LENGTH = 32
RSA_KEY_LENGTH = 2048

def generate_rsa_keys(username, password):
    """Generates a new RSA key pair and saves the encrypted private key."""
    key = RSA.generate(RSA_KEY_LENGTH)

    os.makedirs(KEYS_DIR, exist_ok=True)

    private_key_path = os.path.join(KEYS_DIR, f"{username}_private.pem")

    # Encrypt the private key with the user's password
    encrypted_private_key = key.export_key('PEM', passphrase=password, pkcs=8,
                                           protection="scryptAndAES128-CBC")

    with open(private_key_path, "wb") as f:
        f.write(encrypted_private_key)

    return key.publickey().export_key('PEM')

def encrypt_with_public_key(data, public_key_pem):
    """Encrypts data using an RSA public key."""
    public_key = RSA.import_key(public_key_pem)
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_data = cipher_rsa.encrypt(data)
    return encrypted_data

def decrypt_with_private_key(data, username, password):
    """Decrypts data using a user's password-protected RSA private key."""
    private_key_path = os.path.join(KEYS_DIR, f"{username}_private.pem")
    try:
        with open(private_key_path, "rb") as f:
            private_key_data = f.read()

        private_key = RSA.import_key(private_key_data, passphrase=password)
        cipher_rsa = PKCS1_OAEP.new(private_key)
        decrypted_data = cipher_rsa.decrypt(data)
        return decrypted_data
    except (FileNotFoundError, ValueError, TypeError):
        # ValueError can be raised if the password is wrong
        return None

def generate_key():
    """Generates a secure 256-bit (32-byte) AES key."""
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
    try:
        with open(input_path, 'rb') as f_in:
            iv = f_in.read(16)
            if len(iv) < 16:
                return False
            ciphertext = f_in.read()

        cipher = AES.new(key, AES.MODE_CBC, iv)

        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

        with open(output_path, 'wb') as f_out:
            f_out.write(plaintext)
        return True
    except (ValueError, KeyError):
        return False

def encrypt_data(data, key):
    """Encrypts byte data using AES-256 in CBC mode."""
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    return iv + ciphertext

def decrypt_data(encrypted_data, key):
    """Decrypts byte data encrypted with AES-256 in CBC mode."""
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted_data
    except (ValueError, KeyError):
        return None

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
        return None

def get_file_hash(filepath):
    """Calculates the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()
