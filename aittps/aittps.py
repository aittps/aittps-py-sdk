from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
import os

class AITTPS:
    @staticmethod
    def generate_ecc_key_pair():
        """Generates a new ECC P-521 key pair."""
        private_key = ec.generate_private_key(ec.SECP521R1(), default_backend())
        public_key = private_key.public_key()

        # Serialize keys to PEM format
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return private_pem, public_pem

    @staticmethod
    def derive_public_key_from_private_key(private_pem: bytes):
        """Derives the public key from the given private key."""
        private_key = serialization.load_pem_private_key(private_pem, password=None, backend=default_backend())
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return public_pem

    @staticmethod
    def decrypt_encrypted_symmetric_key(encrypted_msg: bytes, private_pem: bytes):
        """
        Decrypts the symmetric key sent by the client using the server's private key.
        `encrypted_msg` is encrypted with the recipient's public key.
        """
        try:
            # Ensure private key is loaded correctly
            private_key = serialization.load_pem_private_key(
                private_pem, password=None, backend=default_backend()
            )
            # Decrypt the symmetric key using the private key
            decrypted_symmetric_key = private_key.decrypt(
                encrypted_msg,
                padding.PKCS1v15()  # Adjust padding based on your key type
            )
            return decrypted_symmetric_key
        except Exception as e:
            print(f"Error loading or decrypting the private key: {e}")
            raise

    @staticmethod
    def encrypt_data_with_aes(symmetric_key: bytes, public_key: bytes):
        """
        Encrypts data using AES and GCM mode. The AES symmetric key is encrypted
        using the recipient's RSA public key.
        """
        # Ensure the symmetric key is of valid length for AES (e.g., 256 bits)
        if len(symmetric_key) not in [16, 24, 32]:  # AES supports key sizes of 128, 192, or 256 bits
            raise ValueError(f"Invalid AES key size: {len(symmetric_key) * 8} bits.")
        
        # Generate a random IV for AES encryption
        iv = os.urandom(12)  # GCM typically uses a 12-byte IV
        
        # Perform AES encryption in GCM mode
        cipher = Cipher(algorithms.AES(symmetric_key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Example: data to be encrypted (could be your actual data)
        data = b"Sensitive Data"
        encrypted_data = encryptor.update(data) + encryptor.finalize()
        
        # Load the RSA public key
        public_key_obj = serialization.load_pem_public_key(public_key, backend=default_backend())
        
        # Encrypt the symmetric key using RSA (OAEP padding)
        encrypted_symmetric_key = public_key_obj.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return encrypted_data, encrypted_symmetric_key, iv
        
    @staticmethod
    def decrypt_data_with_aes(encrypted_msg: bytes, symmetric_key: bytes):
        """Decrypts encrypted data using the provided AES symmetric key."""
        iv = encrypted_msg[:12]  # Extract the IV
        ciphertext = encrypted_msg[12:-16]  # Extract the ciphertext (after IV and before tag)
        auth_tag = encrypted_msg[-16:]  # Extract the authentication tag (last 16 bytes)

        cipher = Cipher(algorithms.AES(symmetric_key), modes.GCM(iv, auth_tag), backend=default_backend())  # Include auth_tag in the cipher
        decryptor = cipher.decryptor()

        padded_msg = decryptor.update(ciphertext) + decryptor.finalize()

        # Return the decrypted message
        return padded_msg.decode()

    @staticmethod
    def generate_random_aes_key():
        """Generates a random 256-bit AES symmetric key."""
        return os.urandom(32)

