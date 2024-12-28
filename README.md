# AITTPS

**AITTPS** is an open-source security and privacy protocol designed for AI agents to communicate securely over public channels like Twitter, Telegram, or APIs. It ensures that no human, bot, or centralized entity can intercept or eavesdrop on communications, maintaining complete confidentiality and privacy.

---

## Features

- **End-to-End Encryption**: Ensures secure communication between AI agents.
- **Elliptic Curve Cryptography (ECC)**: Utilizes ECC P-521 for generating robust cryptographic keys.
- **AES Encryption**: Secures data using 256-bit AES encryption for speed and security.
- **Random Key Generation**: Generates high-entropy symmetric keys for encrypting data.
- **Interoperability**: Can be integrated with public channels like Twitter, Telegram, APIs, and more.
- **Open Source**: Designed for transparency and extensibility.

---

## Installation

To install AITTPS, use `pip`:

```bash
pip install aittps
```

---

## Getting Started

### 1. Importing AITTPS

```python
from aittps import AITTPS
```

### 2. Generating Key Pairs

Generate a secure ECC key pair:

```python
aittps = AITTPS()
private_key, public_key = aittps.generate_ecc_key_pair()
print("Private Key:", private_key)
print("Public Key:", public_key)
```

### 3. Encrypting and Decrypting Data

#### Encrypt Data:

```python
symmetric_key = aittps.generate_random_aes_key()
data = "Secure message for AI agent."

encrypted_data, encrypted_symmetric_key, iv = aittps.encrypt_data_with_aes(symmetric_key, data.encode())
print("Encrypted Data:", encrypted_data)
```

#### Decrypt Data:

```python
decrypted_data = aittps.decrypt_data_with_aes(encrypted_data, symmetric_key)
print("Decrypted Data:", decrypted_data.decode())
```

### 4. Deriving Public Key from Private Key

```python
derived_public_key = aittps.derive_public_key_from_private_key(private_key)
print("Derived Public Key:", derived_public_key)
```

---

## Use Cases

- **Secure AI Communication**: Protect sensitive data exchanged between AI agents.
- **Public Channel Security**: Encrypt messages sent over public platforms like Twitter or Telegram.
- **API Communication**: Secure API-based interactions with strong cryptography.

---

## Example Workflow

Here’s an example of encrypting a message, sharing it over a public channel, and decrypting it on the receiving end:

1. **Sender Side**:

   ```python
   from aittps import AITTPS

   aittps = AITTPS()
   private_key, public_key = aittps.generate_ecc_key_pair()
   symmetric_key = aittps.generate_random_aes_key()

   message = "This is a secure message."
   encrypted_data, encrypted_symmetric_key, iv = aittps.encrypt_data_with_aes(symmetric_key, message.encode())

   # Share `encrypted_data`, `encrypted_symmetric_key`, and `iv` over a public channel
   print("Encrypted Message Sent.")
   ```

2. **Receiver Side**:

   ```python
   decrypted_symmetric_key = aittps.decrypt_encrypted_symmetric_key(encrypted_symmetric_key, private_key)
   decrypted_message = aittps.decrypt_data_with_aes(encrypted_data, decrypted_symmetric_key)

   print("Decrypted Message:", decrypted_message.decode())
   ```

---

## Contributing

We welcome contributions to AITTPS! If you’d like to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Support

If you encounter any issues or have questions, feel free to open an issue on our [GitHub repository](https://github.com/your-repo/aittps).

---

## Acknowledgments

Special thanks to the open-source community for their contributions and support.

