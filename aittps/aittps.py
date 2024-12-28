from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os


class AITTPS:
    @staticmethod
    def generate_new_key_pair():
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
    def derive_session_key(private_pem: bytes, peer_public_pem: bytes):
        """Derives a shared session key using ECC ECDH."""
        # Load private key
        private_key = serialization.load_pem_private_key(private_pem, password=None, backend=default_backend())
        # Load peer's public key
        peer_public_key = serialization.load_pem_public_key(peer_public_pem, backend=default_backend())
        # Perform ECDH key exchange
        shared_key = private_key.exchange(ec.ECDH(), peer_public_key)
        # Derive a symmetric key using HKDF
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,  # 256-bit key for AES
            salt=None,
            info=b'handshake data',
            backend=default_backend()
        ).derive(shared_key)
        return derived_key

    @staticmethod
    def encrypt_data_with_aes(data: bytes, symmetric_key: bytes):
        """Encrypts data using AES GCM."""
        if len(symmetric_key) not in [16, 24, 32]:  # AES key lengths: 128, 192, or 256 bits
            raise ValueError("Invalid AES key size.")
        iv = os.urandom(12)  # Generate a random IV (12 bytes for GCM)
        cipher = Cipher(algorithms.AES(symmetric_key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()
        return iv + ciphertext + encryptor.tag  # Return IV + encrypted data + GCM tag

    @staticmethod
    def decrypt_data_with_aes(encrypted_data: bytes, symmetric_key: bytes):
        """Decrypts data using AES GCM."""
        iv = encrypted_data[:12]  # Extract the IV
        tag = encrypted_data[-16:]  # Extract the GCM tag
        ciphertext = encrypted_data[12:-16]  # Extract the ciphertext
        cipher = Cipher(algorithms.AES(symmetric_key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
        return decrypted_data

    @staticmethod
    def generate_random_aes_key():
        """Generates a random 256-bit AES symmetric key."""
        return os.urandom(32)


# Example Usage
if __name__ == "__main__":
    # Generate ECC key pair
    private_key, public_key = AITTPS.generate_new_key_pair()

    # Derive shared session key
    peer_private_key, peer_public_key = AITTPS.generate_new_key_pair()
    session_key = AITTPS.derive_session_key(private_key, peer_public_key)
    print(f"Derived Session Key: {session_key.hex()}")

    # Encrypt and decrypt a message
    message = b"Sensitive Data"
    encrypted_message = AITTPS.encrypt_data_with_aes(message, session_key)
    print(f"Encrypted Message: {encrypted_message.hex()}")
    decrypted_message = AITTPS.decrypt_data_with_aes(encrypted_message, session_key)
    print(f"Decrypted Message: {decrypted_message.decode()}")

    # Generate a random AES key
    random_aes_key = AITTPS.generate_random_aes_key()
    print(f"Random AES Key: {random_aes_key.hex()}")
