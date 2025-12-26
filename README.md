# VaultGuard: Secure Password Vault with SSL/TLS-Secured Multi-Factor Authentication

**A secure, cross-platform password vault application with client-side encryption and SSL/TLS-secured TOTP Multi-Factor Authentication.**

---

## 🔐 Project Overview

VaultGuard is a comprehensive security project implementing a password manager with enterprise-grade security features:

- **Client-Side AES-256-GCM Encryption** - All data encrypted locally using keys derived from your Master Password
- **Argon2id Key Derivation** - Industry-standard KDF for secure key generation
- **60-Second TOTP MFA** - Time-based One-Time Passwords for two-factor authentication
- **SSL/TLS Secured Communication** - All network traffic encrypted using HTTPS
- **SHA-256 Integrity Verification** - Detect any tampering with vault files
- **Dual Transfer OTP Mechanism** - Server generates OTPs accessible by both mobile and desktop apps

---

## 🎯 Key Features

### Security Components

1. **Master Password Authentication**
   - Argon2id key derivation function (KDF)
   - Salted password hashing
   - Never transmitted in plaintext

2. **Client-Side Encryption**
   - AES-256-GCM symmetric encryption
   - All credentials encrypted locally
   - Single encrypted vault file storage

3. **Multi-Factor Authentication (MFA)**
   - TOTP (Time-based One-Time Password) protocol
   - 60-second validity window
   - Dedicated MFA server
   - Mobile authenticator app (GUI + CLI)

4. **Secure Communication**
   - SSL/TLS (HTTPS) for all network traffic
   - Self-signed certificates for development
   - Production-ready certificate support

5. **Data Integrity**
   - SHA-256 hash verification
   - Detects unauthorized file tampering
   - Automatic integrity checks on load

---

## 📋 System Requirements

### Prerequisites
- Python 3.8 or higher
- Windows OS (batch scripts included)
- Virtual environment support

### Python Dependencies
```
cryptography
argon2-cffi
flask
requests
pyotp
urllib3
pyperclip
```

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/AliTarek-1/security.git
cd security

# Install dependencies
install_deps.bat
```

### 2. Running the System

**Option A: GUI Version (Recommended)**
```bash
start_gui.bat
```
This launches:
- MFA Server (HTTPS on port 5000)
- Mobile Authenticator GUI
- VaultGuard Password Manager GUI

**Option B: Console Version**
```bash
start_system.bat
```
This launches command-line interfaces for all components.

### 3. First-Time Setup

1. **Register in Mobile App**
   - Open Mobile Authenticator
   - Click "Register New Device"
   - Enter username (e.g., "bob")
   - Save the secret displayed

2. **Get OTP Code**
   - Click on your username in the mobile app
   - Note the 6-digit OTP code
   - Code refreshes every 60 seconds

3. **Login to VaultGuard**
   - Open VaultGuard Password Manager
   - Enter Master Password (create new one)
   - Enter username (same as mobile app)
   - Enter current OTP code
   - Access granted!

---

## 🏗️ System Architecture

### Components

#### 1. VaultGuard Client (`vault_gui.py`)
- Main password manager interface
- Handles master password authentication
- Encrypts/decrypts vault data locally
- Communicates with MFA server for authentication

#### 2. MFA Server (`mfa_server.py`)
- Flask-based HTTPS server
- Manages user registration
- Generates and validates TOTP codes
- Dual transfer OTP mechanism

#### 3. Mobile Authenticator (`mobile_auth_gui.py`)
- User-friendly GUI for OTP display
- Saves registered users locally
- Live OTP countdown timer
- Copy to clipboard support

#### 4. Cryptography Module (`crypto_manager.py`)
- Argon2id password hashing
- AES-256-GCM encryption/decryption
- Key derivation functions
- Data integrity verification

#### 5. Vault File Manager (`vault_file_manager.py`)
- Secure file I/O operations
- SHA-256 integrity checking
- JSON-based encrypted storage

### Data Flow

```
┌─────────────────┐     HTTPS     ┌──────────────┐
│  Mobile Auth    │◄─────────────►│  MFA Server  │
│      App        │   Register     │   (HTTPS)    │
└─────────────────┘   Get OTP      └──────────────┘
                                           ▲
                                           │ HTTPS
                                           │ Verify OTP
                                           ▼
┌─────────────────┐              ┌──────────────┐
│   VaultGuard    │              │ Encrypted    │
│     Client      │◄────────────►│ Vault File   │
│   (GUI/CLI)     │   AES-256    │  (vault.dat) │
└─────────────────┘   Argon2     └──────────────┘
```

---

## 🔬 Testing

### Run All Tests
```bash
run_tests.bat
```

### Individual Test Suites
```bash
# Test cryptography
python -m unittest tests.test_crypto

# Test Argon2 KDF
python -m unittest tests.test_argon2

# Test MFA/TOTP
python -m unittest tests.test_mfa

# Test vault integrity
python -m unittest tests.test_vault

# Integration tests
python -m unittest tests.test_integration
```

### Test Coverage
- ✅ AES-256-GCM encryption/decryption
- ✅ Argon2id key derivation
- ✅ TOTP 60-second interval
- ✅ OTP generation and verification
- ✅ Vault file integrity
- ✅ Tampering detection
- ✅ End-to-end workflow

---

## 📊 Security Analysis

### Encryption Standards
- **Algorithm**: AES-256-GCM (Galois/Counter Mode)
- **Key Size**: 256 bits
- **Authentication**: Built-in AEAD (Authenticated Encryption with Associated Data)

### Key Derivation
- **Function**: Argon2id (hybrid version)
- **Memory**: 64 MB
- **Iterations**: 3
- **Parallelism**: 4 threads
- **Salt**: 16 bytes random

### MFA Implementation
- **Protocol**: TOTP (RFC 6238)
- **Interval**: 60 seconds
- **Algorithm**: HMAC-SHA1
- **Code Length**: 6 digits

### Integrity Verification
- **Hash**: SHA-256
- **Coverage**: Entire vault file
- **Verification**: On every load

---

## 💾 File Structure

```
security/
├── crypto_manager.py       # Cryptographic operations
├── vault_file_manager.py   # File I/O and integrity
├── mfa_server.py           # MFA HTTPS server
├── mfa_client.py           # MFA client library
├── mobile_auth_gui.py      # Mobile app (GUI)
├── mobile_auth_app.py      # Mobile app (CLI)
├── vault_gui.py            # Password manager (GUI)
├── main.py                 # Password manager (CLI)
├── start_gui.bat           # Launch GUI version
├── start_system.bat        # Launch CLI version
├── run_tests.bat           # Run test suite
├── requirements.txt        # Python dependencies
├── vault.dat               # Encrypted vault (generated)
├── mfa_db.json             # MFA user database
├── mobile_users.json       # Mobile app saved users
└── tests/
    ├── test_crypto.py      # Encryption tests
    ├── test_argon2.py      # KDF tests
    ├── test_mfa.py         # TOTP tests
    ├── test_vault.py       # File integrity tests
    └── test_integration.py # End-to-end tests
```

---

## 🛡️ Security Best Practices Implemented

✅ **Never store passwords in plaintext**
✅ **Use strong KDF (Argon2id) for key derivation**
✅ **Implement proper salting for password hashes**
✅ **Encrypt all sensitive data at rest**
✅ **Use authenticated encryption (AEAD)**
✅ **Secure all network communication with SSL/TLS**
✅ **Implement integrity checking**
✅ **Use time-based one-time passwords for 2FA**
✅ **Validate all user inputs**
✅ **Handle errors securely without leaking information**

---

## 🚧 Known Limitations

1. **Single-user application** - Not designed for multi-user scenarios
2. **Self-signed certificates** - Development uses adhoc SSL (production needs proper certs)
3. **Local storage only** - No cloud sync capability
4. **Windows-focused** - Batch scripts are Windows-specific
5. **No password strength meter** - Users must choose strong passwords
6. **No account recovery** - Lost master password means lost data

---

## 📚 Technologies Used

- **Python 3.x** - Primary language
- **Flask** - MFA server framework
- **cryptography** - AES-GCM encryption
- **argon2-cffi** - Argon2 key derivation
- **pyotp** - TOTP implementation
- **tkinter** - GUI framework
- **unittest** - Testing framework

---

## 🎓 Learning Outcomes

This project demonstrates:
- Secure password management implementation
- Client-side encryption best practices
- Multi-factor authentication systems
- SSL/TLS secured communication
- Key derivation functions (KDF)
- Hash-based integrity verification
- Time-based one-time password (TOTP) protocol
- Agile development methodology
- Comprehensive testing strategies

---

## 👥 Contributors

- **Ali Tarek** - Project Lead & Implementation
- **Omar Tamer** - Core Development & Security Features
- **Fatma Ayman** - Backend Development & MFA
- **Ahmed El-Baramouny** - Security Analysis & Testing
- **Ahmed Mohamed** - GUI Development & Documentation
- Course: Information Security
- Institution: [Your University Name]
- Date: December 2025

---

## 📄 License

This project is for educational purposes as part of an Information Security course.

---

## 🆘 Troubleshooting

### Issue: "Could not connect to MFA Server"
**Solution**: Make sure `mfa_server.py` is running first
```bash
python mfa_server.py
```

### Issue: "Invalid or expired OTP"
**Solution**: 
- Check that OTP is entered within 60 seconds
- Ensure system clocks are synchronized
- Verify you're using the correct username

### Issue: "Failed to decrypt vault"
**Solution**:
- Verify you're using the correct master password
- If password is lost, delete `vault.dat` to start fresh
- Check that vault file hasn't been corrupted

### Issue: SSL/TLS certificate errors
**Solution**:
- Install pyOpenSSL: `pip install pyopenssl`
- Allow self-signed certificates in development
- For production, use proper SSL certificates

---


**Built with security in mind. Keep your passwords safe! 🔐**