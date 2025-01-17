import base64
import os
import random
import string
import bcrypt

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def random_string(length: int) -> str:
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length))


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def compare_passwords(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def validate_password(password: str):
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    return True


AES_KEY = os.urandom(32)
NONCE_SIZE = 12


def encrypt_str(plaintext: str) -> str:
    try:
        # Generate a random nonce
        nonce = os.urandom(NONCE_SIZE)

        # Initialize AES-GCM with the key
        aesgcm = AESGCM(AES_KEY)

        # Encrypt the plaintext
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)

        # Combine nonce and ciphertext
        combined = nonce + ciphertext

        # Encode to Base64 for safe storage/transmission
        ciphertext_base64 = base64.urlsafe_b64encode(combined).decode()
        return ciphertext_base64
    except Exception as e:
        raise RuntimeError(f"Encryption failed: {e}")


def decrypt_str(ciphertext_base64: str) -> str:
    try:
        # Decode the Base64-encoded ciphertext
        combined = base64.urlsafe_b64decode(ciphertext_base64)

        # Extract the nonce and ciphertext
        nonce, ciphertext = combined[:NONCE_SIZE], combined[NONCE_SIZE:]

        # Initialize AES-GCM with the key
        aesgcm = AESGCM(AES_KEY)

        # Decrypt the ciphertext
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode()
    except Exception as e:
        raise RuntimeError(f"Decryption failed: {e}")