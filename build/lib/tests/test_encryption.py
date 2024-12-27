import unittest
from aittps import AITTPS  # Assuming your SDK is named aittps

class TestAITTPS(unittest.TestCase):
    def setUp(self):
        """Set up test data before each test."""
        self.aittps = AITTPS()

    def test_generate_ecc_key_pair(self):
        """Test the generation of ECC P-521 key pair."""
        private_key, public_key = self.aittps.generate_ecc_key_pair()

        # Check that private and public keys are not empty
        self.assertIsNotNone(private_key)
        self.assertIsNotNone(public_key)

        # Check that the keys are in PEM format (starts with '-----BEGIN' and ends with '-----END')
        self.assertTrue(private_key.startswith(b"-----BEGIN PRIVATE KEY-----"))
        self.assertTrue(public_key.startswith(b"-----BEGIN PUBLIC KEY-----"))

    def test_derive_public_key_from_private_key(self):
        """Test deriving the public key from the private key."""
        private_key, _ = self.aittps.generate_ecc_key_pair()
        derived_public_key = self.aittps.derive_public_key_from_private_key(private_key)

        # Ensure the derived public key is in PEM format
        self.assertTrue(derived_public_key.startswith(b"-----BEGIN PUBLIC KEY-----"))

    def test_decrypt_encrypted_symmetric_key(self):
        """Test decrypting the symmetric key."""
        # Generate public/private key pair for sender and receiver
        private_key, public_key = self.aittps.generate_ecc_key_pair()

        # Encrypt a random symmetric key using the receiver's public key
        symmetric_key = self.aittps.generate_random_aes_key()
        encrypted_data, encrypted_symmetric_key, iv = self.aittps.encrypt_data_with_aes(symmetric_key, public_key)

        # Now decrypt using the private key (ensure correct private key format)
        decrypted_symmetric_key = self.aittps.decrypt_encrypted_symmetric_key(
            encrypted_symmetric_key, private_key
        )
        
        # Ensure the decrypted symmetric key matches the original one
        self.assertEqual(symmetric_key, decrypted_symmetric_key)

    def test_encrypt_and_decrypt_data(self):
        """Test encrypting and decrypting data with AES."""
        # Generate symmetric key
        symmetric_key = self.aittps.generate_random_aes_key()

        raw_message = "Test encryption and decryption"
        encrypted_data, encrypted_symmetric_key, iv = self.aittps.encrypt_data_with_aes(symmetric_key, raw_message.encode())
        
        # Decrypt the encrypted message
        decrypted_msg = self.aittps.decrypt_data_with_aes(encrypted_data, symmetric_key)

        # Ensure the decrypted message matches the original
        self.assertEqual(raw_message, decrypted_msg)

    def test_generate_random_aes_key(self):
        """Test generating a random AES key."""
        symmetric_key = self.aittps.generate_random_aes_key()

        # Ensure that the symmetric key is 32 bytes (256-bit)
        self.assertEqual(len(symmetric_key), 32)
        self.assertTrue(isinstance(symmetric_key, bytes))

if __name__ == "__main__":
    unittest.main()
