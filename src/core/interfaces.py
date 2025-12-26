# FILE: interfaces.py
import json
import time

class CryptoManagerStub:
    """
    TEMPORARY STUB for Member 2 (Cryptography).
    """
    def encrypt_data(self, plaintext_list, master_password):
        # Placeholder: Just dumps JSON to bytes (No real encryption yet)
        print("[DEBUG-STUB] Member 2: Encrypting data (Simulated)...")
        return json.dumps(plaintext_list).encode('utf-8')

    def decrypt_data(self, ciphertext_bytes, master_password):
        # Placeholder: Just loads JSON from bytes
        print("[DEBUG-STUB] Member 2: Decrypting data (Simulated)...")
        try:
            return json.loads(ciphertext_bytes.decode('utf-8'))
        except:
            return []

class MFAServiceStub:
    """
    TEMPORARY STUB for Member 3/4 (MFA Server).
    """
    def perform_login(self):
        print("\n[DEBUG-STUB] Member 3: Connecting to MFA Server...")
        print("[DEBUG-STUB] Member 3: Verifying TOTP Code...")
        time.sleep(1) # Simulate network delay
        print("[DEBUG-STUB] Member 3: Access Granted.")
        return True