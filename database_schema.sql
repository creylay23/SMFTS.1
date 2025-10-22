-- database_schema.sql

-- This script defines the database schema for the Secure File and Message Transfer System.
-- It creates a 'users' table to store user credentials and roles.

-- Drop the table if it already exists to ensure a clean setup
DROP TABLE IF EXISTS users;

-- Create the 'users' table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('Admin', 'Doctor', 'Nurse'))
);

-- Note: The password_hash column will store passwords hashed with bcrypt.
-- The role column is restricted to the three specified roles.
