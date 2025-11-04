import sqlite3
import os

DATABASE_FILE = "secure_app.db"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Creates the database tables from the schema file if the db doesn't exist."""
    if os.path.exists(DATABASE_FILE):
        return  # Database already exists

    conn = get_db_connection()
    with open('database_schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.close()

def add_user(username, password_hash, role, public_key):
    """Adds a new user to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role, public_key) VALUES (?, ?, ?, ?)",
            (username, password_hash, role, public_key)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

def get_user(username):
    """Retrieves a user from the database by username."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_all_users():
    """Retrieves all users from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def get_public_key(username):
    """Retrieves a user's public key."""
    user = get_user(username)
    return user['public_key'] if user else None

def save_message(sender, recipient, encrypted_message, encrypted_key):
    """Saves a secure message to the database."""
    conn = get_db_connection()
    conn.execute("INSERT INTO secure_messages (sender_username, recipient_username, encrypted_message, encrypted_session_key) VALUES (?, ?, ?, ?)",
                 (sender, recipient, encrypted_message, encrypted_key))
    conn.commit()
    conn.close()

def get_messages_for_user(username):
    """Retrieves all messages for a given user."""
    conn = get_db_connection()
    messages = conn.execute("SELECT * FROM secure_messages WHERE recipient_username = ?", (username,)).fetchall()
    conn.close()
    return messages

def save_file(sender, recipient, filename, encrypted_file, encrypted_key):
    """Saves a secure file to the database."""
    conn = get_db_connection()
    conn.execute("INSERT INTO secure_files (sender_username, recipient_username, filename, encrypted_file, encrypted_session_key) VALUES (?, ?, ?, ?, ?)",
                 (sender, recipient, filename, encrypted_file, encrypted_key))
    conn.commit()
    conn.close()

def get_files_for_user(username):
    """Retrievel all files for a given user."""
    conn = get_db_connection()
    files = conn.execute("SELECT * FROM secure_files WHERE recipient_username = ?", (username,)).fetchall()
    conn.close()
    return files
