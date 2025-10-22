import bcrypt
import database

def hash_password(password):
    """Hashes a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed_password):
    """Checks if a password matches its hashed version."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def create_user(username, password, role):
    """Creates a new user with a hashed password."""
    if not all([username, password, role]):
        return False, "All fields are required."

    hashed_password = hash_password(password)
    success = database.add_user(username, hashed_password, role)
    if not success:
        return False, "Username already exists."
    return True, "User created successfully."

def authenticate_user(username, password):
    """Authenticates a user by checking their username and password."""
    user = database.get_user(username)
    if user and check_password(password, user['password_hash']):
        return True, user['role']
    return False, None
