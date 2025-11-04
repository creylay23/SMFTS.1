import unittest
import os
import encryption

class TestEncryption(unittest.TestCase):

    def setUp(self):
        """Set up for the tests."""
        self.key = encryption.generate_key()
        self.test_dir = "test_data"
        os.makedirs(self.test_dir, exist_ok=True)

        self.original_file = os.path.join(self.test_dir, "original.txt")
        self.encrypted_file = os.path.join(self.test_dir, "encrypted.bin")
        self.decrypted_file = os.path.join(self.test_dir, "decrypted.txt")

        with open(self.original_file, "w") as f:
            f.write("This is a secret test file for encryption.")

    def tearDown(self):
        """Clean up the test files."""
        for file_path in [self.original_file, self.encrypted_file, self.decrypted_file]:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.rmdir(self.test_dir)

    def test_key_generation(self):
        """Test that the generated key has the correct length (32 bytes for AES-256)."""
        self.assertEqual(len(self.key), 32)

    def test_message_encryption_decryption(self):
        """Test that a message can be encrypted and then decrypted successfully."""
        message = "This is a secret message."
        encrypted_message = encryption.encrypt_message(message, self.key)
        decrypted_message = encryption.decrypt_message(encrypted_message, self.key)
        self.assertEqual(message, decrypted_message)

    def test_file_encryption_decryption(self):
        """Test that a file can be encrypted and then decrypted successfully."""
        encryption.encrypt_file(self.original_file, self.encrypted_file, self.key)
        self.assertTrue(os.path.exists(self.encrypted_file))

        success = encryption.decrypt_file(self.encrypted_file, self.decrypted_file, self.key)
        self.assertTrue(success)

        with open(self.original_file, "r") as f1, open(self.decrypted_file, "r") as f2:
            self.assertEqual(f1.read(), f2.read())

    def test_decryption_with_wrong_key(self):
        """Test that decryption fails when using an incorrect key."""
        wrong_key = encryption.generate_key()

        # Test message decryption
        message = "Another secret message"
        encrypted_message = encryption.encrypt_message(message, self.key)
        decrypted_message = encryption.decrypt_message(encrypted_message, wrong_key)
        self.assertIsNone(decrypted_message)

        # Test file decryption
        encryption.encrypt_file(self.original_file, self.encrypted_file, self.key)
        success = encryption.decrypt_file(self.encrypted_file, self.decrypted_file, wrong_key)
        self.assertFalse(success)

    def test_file_hash(self):
        """Test the SHA-256 file hash function."""
        expected_hash = "06799e9410e5d828e24d04bdf1ed0c92bf059b80619e33a696707beb61f187a6"
        actual_hash = encryption.get_file_hash(self.original_file)
        self.assertEqual(expected_hash, actual_hash)

if __name__ == '__main__':
    unittest.main()
