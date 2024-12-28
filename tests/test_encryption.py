import unittest
from aittps import AITTPS  # Assuming your SDK is named aittps


class TestAITTPS(unittest.TestCase):
    def setUp(self):
        """Set up test data before each test."""
        self.aittps = AITTPS()

    def test_generate_ecc_key_pair(self):
        """Test the generation of ECC P-521 key pair."""
        private_key, public_key = self.aittps.generate_new_key_pair()

        # Check that private and public keys are not empty
        self.assertIsNotNone(private_key)
        self.assertIsNotNone(public_key)

        # Check that the keys are in PEM format (starts with '-----BEGIN' and ends with '-----END')
        self.assertTrue(private_key.startswith(b"-----BEGIN PRIVATE KEY-----"))
        self.assertTrue(public_key.startswith(b"-----BEGIN PUBLIC KEY-----"))

    def test_derive_public_key_from_private_key(self):
        """Test deriving the public key from the private key."""
        private_key, _ = self.aittps.generate_new_key_pair()
        derived_public_key = self.aittps.derive_public_key_from_private_key(private_key)

        # Ensure the derived public key is in PEM format
        self.assertTrue(derived_public_key.startswith(b"-----BEGIN PUBLIC KEY-----"))

    def test_derive_session_key(self):
        """Test deriving a session key from ECC key pairs."""
        private_key_1, public_key_1 = self.aittps.generate_new_key_pair()
        private_key_2, public_key_2 = self.aittps.generate_new_key_pair()

        session_key_1 = self.aittps.derive_session_key(private_key_1, public_key_2)
        session_key_2 = self.aittps.derive_session_key(private_key_2, public_key_1)

        # Ensure the session keys derived by both parties match
        self.assertEqual(session_key_1, session_key_2)

    def test_encrypt_and_decrypt_data(self):
        """Test encrypting and decrypting data with AES."""
        symmetric_key = self.aittps.generate_random_aes_key()
        message = b"Test encryption and decryption"

        encrypted_data = self.aittps.encrypt_data_with_aes(message, symmetric_key)
        decrypted_message = self.aittps.decrypt_data_with_aes(encrypted_data, symmetric_key)

        # Ensure the decrypted message matches the original
        self.assertEqual(message, decrypted_message)

    def test_generate_random_aes_key(self):
        """Test generating a random AES key."""
        symmetric_key = self.aittps.generate_random_aes_key()

        # Ensure the symmetric key is 32 bytes (256 bits)
        self.assertEqual(len(symmetric_key), 32)
        self.assertIsInstance(symmetric_key, bytes)


if __name__ == "__main__":
    unittest.main()
