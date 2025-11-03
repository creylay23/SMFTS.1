import bcrypt
import database
import encryption

def hash_password(password):
    """Hashes a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed_password):
    """Checks if a password matches its hashed version."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def create_user(username, password, role):
    """Creates a new user, generates RSA keys, and stores the public key."""
    if not all([username, password, role]):
        return False, "All fields are required."

    # Generate RSA keys first, encrypting the private key with the user's password
    public_key_pem = encryption.generate_rsa_keys(username, password)

    hashed_password = hash_password(password)

    # Now, add the user with their public key
    success = database.add_user(username, hashed_password, role, public_key_pem)

    if not success:
        # If user creation fails, we should ideally clean up the generated key files.
        # For simplicity in this context, we'll note this as a point for future improvement.
        return False, "Username already exists."

    return True, "User created successfully."

def authenticate_user(username, password):
    """Authenticates a user by checking their username and password."""
    user = database.get_user(username)
    if user and check_password(password, user['password_hash']):
        return True, user['role']
    return False, None
