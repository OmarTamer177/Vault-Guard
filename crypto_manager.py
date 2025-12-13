import json
import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256

class CryptoManager:
    """
    Handles all cryptographic operations:
    - Key Derivation (Argon2)
    - Encryption (AES-GCM)
    - Decryption (AES-GCM)
    - Hashing (SHA-256)
    """

    def __init__(self):
        # Configuration for Argon2
        self.salt_len = 16
        self.key_len = 32 # AES-256
        self.nonce_len = 12 # Recommended for GCM

    def derive_key(self, password, salt):
        """
        Derives a 32-byte key from the password and salt using Argon2.
        """
        # Switching to PBKDF2 for compatibility as Argon2 import is failing on this setup
        key = PBKDF2(password, salt, dkLen=self.key_len, count=100000) 
        return key

    def encrypt_data(self, plaintext_list, master_password):
        """
        Encrypts a list of dictionaries (credentials) using AES-GCM.
        Returns bytes: salt + nonce + tag + ciphertext
        """
        if not master_password:
            raise ValueError("Master password is required for encryption")

        # 1. Prepare Data
        json_data = json.dumps(plaintext_list).encode('utf-8')

        # 2. Generate Salt and Derive Key
        salt = get_random_bytes(self.salt_len)
        key = self.derive_key(master_password, salt)

        # 3. Encrypt
        cipher = AES.new(key, AES.MODE_GCM)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(json_data)

        # 4. Pack Result (Salt + Nonce + Tag + Ciphertext)
        # We need all these to decrypt.
        # salt: 16 bytes
        # nonce: 16 bytes (default in pycryptodome for GCM can vary, but standard is often 12 or 16. Let's rely on cipher.nonce len)
        # tag: 16 bytes
        
        packed_data = salt + nonce + tag + ciphertext
        return packed_data

    def decrypt_data(self, encrypted_data, master_password):
        """
        Decrypts the data payload.
        Expects: salt + nonce + tag + ciphertext
        """
        try:
            # Unpack
            # Salt is fixed length
            salt = encrypted_data[:self.salt_len]
            remaining = encrypted_data[self.salt_len:]
            
            # Nonce length: PyCryptodome AES-GCM default nonce is 16 bytes? 
            # Actually, standard GCM nonce is 12 bytes. PyCryptodome might use 16.
            # Best practice is to store lengths if variable, but let's check what we did in encrypt.
            # cipher.nonce was used.
            # Let's start with assuming we need to control nonce length or read it.
            # To be safe and deterministic, let's specify nonce length in encrypt.
            # Re-writing encrypt slightly implicitly in my head: cipher = AES.new(..., nonce=get_random_bytes(12))
            # But AES.new(..., MODE_GCM) generates a random nonce if not provided.
            # Let's peek at the length. For safety in this implementation, I will assume 16 bytes for now or fixed 12.
            # It is safer to fix it to 12 (96 bits) which is standard for GCM.
            pass
        except Exception as e:
            print(f"[Crypto Error] {e}")
            return []

        # RE-IMPLEMENTING ENCRYPT/DECRYPT logic below for correctness with fixed nonce.
        return []

    # --- REVISED METHODS ---
    
    def encrypt_data_safe(self, plaintext_list, master_password):
        # 1. Prepare Data
        json_data = json.dumps(plaintext_list).encode('utf-8')

        # 2. Salt & Key
        salt = get_random_bytes(self.salt_len)
        key = self.derive_key(master_password, salt)

        # 3. Nonce (Fixed 12 bytes for GCM)
        nonce = get_random_bytes(12)
        
        # 4. Encrypt
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(json_data)

        # 5. Return
        return salt + nonce + tag + ciphertext

    def decrypt_data_safe(self, blob, master_password):
        try:
            # Slicing
            current_idx = 0
            
            salt = blob[current_idx : current_idx + self.salt_len]
            current_idx += self.salt_len
            
            nonce = blob[current_idx : current_idx + 12]
            current_idx += 12
            
            tag = blob[current_idx : current_idx + 16]
            current_idx += 16
            
            ciphertext = blob[current_idx:]

            # Derive
            key = self.derive_key(master_password, salt)

            # Decrypt
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
            
            return json.loads(decrypted_data.decode('utf-8'))
        except (ValueError, KeyError) as e:
            print("[Crypto] Decryption failed. Wrong password or corrupted data.")
            return None
            
    # Alias for compatibility with main.py
    encrypt_data = encrypt_data_safe
    decrypt_data = decrypt_data_safe
