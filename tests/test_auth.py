import unittest
import os
import sqlite3
import auth
import database

class TestAuth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up a temporary database for testing."""
        database.DATABASE_FILE = "test_secure_app.db"
        database.create_tables()

    @classmethod
    def tearDownClass(cls):
        """Remove the temporary database after tests."""
        os.remove(database.DATABASE_FILE)

    def tearDown(self):
        """Clear the users table after each test."""
        conn = database.get_db_connection()
        conn.execute("DELETE FROM users")
        conn.commit()
        conn.close()

    def test_password_hashing(self):
        """Test that password hashing and checking work correctly."""
        password = "securepassword123"
        hashed_password = auth.hash_password(password)
        self.assertTrue(auth.check_password(password, hashed_password))
        self.assertFalse(auth.check_password("wrongpassword", hashed_password))

    def test_create_user(self):
        """Test creating a new user."""
        success, message = auth.create_user("testuser", "password", "Doctor")
        self.assertTrue(success)
        self.assertEqual(message, "User created successfully.")

        user = database.get_user("testuser")
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], "testuser")
        self.assertEqual(user['role'], "Doctor")

    def test_create_duplicate_user(self):
        """Test that creating a user with a duplicate username fails."""
        auth.create_user("testuser", "password", "Doctor")
        success, message = auth.create_user("testuser", "password", "Nurse")
        self.assertFalse(success)
        self.assertEqual(message, "Username already exists.")

    def test_authenticate_user(self):
        """Test that user authentication works with correct credentials."""
        auth.create_user("testuser", "password123", "Admin")
        authenticated, role = auth.authenticate_user("testuser", "password123")
        self.assertTrue(authenticated)
        self.assertEqual(role, "Admin")

    def test_authenticate_user_wrong_password(self):
        """Test that authentication fails with an incorrect password."""
        auth.create_user("testuser", "password123", "Admin")
        authenticated, role = auth.authenticate_user("testuser", "wrongpassword")
        self.assertFalse(authenticated)
        self.assertIsNone(role)

    def test_authenticate_nonexistent_user(self):
        """Test that authentication fails for a user that does not exist."""
        authenticated, role = auth.authenticate_user("nonexistent", "password")
        self.assertFalse(authenticated)
        self.assertIsNone(role)

if __name__ == '__main__':
    unittest.main()
