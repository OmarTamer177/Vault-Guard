import sys
import os

print("--- DIAGNOSTICS ---")
print(f"Python Executable: {sys.executable}")
print(f"Working Directory: {os.getcwd()}")
print("System Path:")
for p in sys.path:
    print(f"  {p}")

print("\nAttempting Import...")
try:
    import Crypto
    print(f"SUCCESS: Crypto module found at {Crypto.__path__}")
    from Crypto.Cipher import AES
    print("SUCCESS: AES imported.")
except ImportError as e:
    print(f"FAILURE: {e}")

try:
    import flask
    print(f"SUCCESS: Flask module found at {flask.__path__}")
except ImportError as e:
    print(f"FAILURE: {e}")
