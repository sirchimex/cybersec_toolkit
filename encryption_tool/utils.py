"""
Encryption utilities for XOR and AES operations.
Security note: XOR is for demonstration only - NOT secure for production.
AES-256-CBC is used for real encryption.
"""
import os
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


# --- XOR Encryption (educational, not secure) ---

def xor_encrypt(plaintext: str, key: str) -> str:
    """XOR encrypt plaintext with key, returning base64-encoded ciphertext."""
    if not key:
        raise ValueError("Key cannot be empty")
    key_bytes = key.encode('utf-8')
    text_bytes = plaintext.encode('utf-8')
    encrypted = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(text_bytes)])
    return base64.b64encode(encrypted).decode('utf-8')


def xor_decrypt(ciphertext_b64: str, key: str) -> str:
    """XOR decrypt base64-encoded ciphertext with key."""
    if not key:
        raise ValueError("Key cannot be empty")
    try:
        ciphertext = base64.b64decode(ciphertext_b64)
    except Exception:
        raise ValueError("Invalid base64 ciphertext")
    key_bytes = key.encode('utf-8')
    decrypted = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(ciphertext)])
    return decrypted.decode('utf-8')


# --- AES-256-CBC Encryption (secure) ---

def _derive_key(password: str) -> bytes:
    """Derive a 32-byte AES key from a password using SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).digest()


def aes_encrypt(plaintext: str, password: str) -> str:
    """
    AES-256-CBC encrypt plaintext with password.
    Output format: base64(IV + ciphertext)
    """
    key = _derive_key(password)
    iv = os.urandom(16)  # Random IV for each encryption
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(plaintext.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded)
    # Prepend IV to ciphertext, then base64 encode
    return base64.b64encode(iv + ciphertext).decode('utf-8')


def aes_decrypt(ciphertext_b64: str, password: str) -> str:
    """AES-256-CBC decrypt base64-encoded ciphertext with password."""
    key = _derive_key(password)
    try:
        data = base64.b64decode(ciphertext_b64)
    except Exception:
        raise ValueError("Invalid base64 ciphertext")
    if len(data) < 16:
        raise ValueError("Ciphertext too short")
    iv = data[:16]
    ciphertext = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted.decode('utf-8')
    except Exception:
        raise ValueError("Decryption failed: wrong key or corrupted data")
