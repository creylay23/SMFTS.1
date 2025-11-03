-- database_schema.sql

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS secure_messages;
DROP TABLE IF EXISTS secure_files;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('Admin', 'Doctor', 'Nurse')),
    public_key TEXT NOT NULL
);

CREATE TABLE secure_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_username TEXT NOT NULL,
    recipient_username TEXT NOT NULL,
    encrypted_message BLOB NOT NULL,
    encrypted_session_key BLOB NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_username) REFERENCES users(username),
    FOREIGN KEY (recipient_username) REFERENCES users(username)
);

CREATE TABLE secure_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_username TEXT NOT NULL,
    recipient_username TEXT NOT NULL,
    filename TEXT NOT NULL,
    encrypted_file BLOB NOT NULL,
    encrypted_session_key BLOB NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_username) REFERENCES users(username),
    FOREIGN KEY (recipient_username) REFERENCES users(username)
);
