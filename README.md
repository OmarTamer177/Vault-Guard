# 🔐 VaultGuard

**Secure Password Vault with Client-Side Encryption & SSL/TLS-Secured Multi-Factor Authentication**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Encryption](https://img.shields.io/badge/Encryption-AES--256--GCM-2ea44f?style=flat-square)](https://en.wikipedia.org/wiki/Galois/Counter_Mode)
[![KDF](https://img.shields.io/badge/KDF-Argon2id-blue?style=flat-square)](https://en.wikipedia.org/wiki/Argon2)
[![MFA](https://img.shields.io/badge/MFA-TOTP%20(60s)-orange?style=flat-square)](https://tools.ietf.org/html/rfc6238)
[![GUI](https://img.shields.io/badge/GUI-CustomTkinter-8A2BE2?style=flat-square)](https://github.com/TomSchimansky/CustomTkinter)

---

## 📖 Overview

**VaultGuard** is a robust, cross-platform password management system built from the ground up with defense-in-depth principles. It pairs a modern desktop password manager with client-side cryptography and an external, TLS-secured Time-based One-Time Password (TOTP) authenticator application.

* **Client-Side AES-256-GCM Encryption** — Sensitive credentials are encrypted and decrypted strictly on your local machine using keys derived from your Master Password.
* **Argon2id Key Derivation** — Industry-standard, memory-hard key derivation to guard against brute-force and GPU/ASIC attacks.
* **Dual-Transfer 60-Second TOTP MFA** — Dedicated authentication service generates and verifies synchronized time-based one-time tokens.
* **SSL/TLS Secured Communications** — All network communications between the desktop client, mobile authenticator, and the auth server run exclusively over HTTPS.
* **Cryptographic Integrity Verification** — SHA-256 hash checksums ensure instant detection of any unauthorized external tampering with vault data.
* **Modern High-Contrast Dark GUI** — Sleek desktop and mobile authenticator interfaces built with CustomTkinter.

---

## 🎯 Architecture & Data Flow

```
┌─────────────────┐             HTTPS              ┌──────────────┐
│  Mobile Auth    │ ◄────────────────────────────► │  MFA Server  │
│      App        │   Register / Fetch Sync OTP    │   (HTTPS)    │
└─────────────────┘                                └──────────────┘
                                                           ▲
                                                           │ HTTPS
                                                           │ Verify OTP
                                                           ▼
┌─────────────────┐                                ┌──────────────┐
│   VaultGuard    │                                │ Encrypted    │
│     Client      │ ◄────────────────────────────► │ Vault File   │
│   (GUI / CLI)   │       AES-256-GCM / Argon2     │ (vault.dat)  │
└─────────────────┘                                └──────────────┘
```

### Core Components

1. **VaultGuard Desktop Client (`src/gui/vault_gui.py`)**  
   The primary application window. Manages master password authentication, credentials CRUD, search, local AES encryption/decryption, and MFA handshake.
2. **MFA Authentication Server (`src/auth/mfa_server.py`)**  
   Flask-based HTTPS microservice providing user registration, TOTP secret generation, and verification over a 60-second window.
3. **Mobile Authenticator Simulator (`src/gui/mobile_auth_gui.py`)**  
   A smartphone-styled companion GUI for generating and viewing live 6-digit TOTP codes with an active countdown timer.
4. **Cryptography Engine (`src/core/crypto_manager.py`)**  
   Handles Argon2id salt generation, key stretching, AES-GCM tag verification, and authenticated payloads.
5. **Secure Vault Storage (`src/core/vault_file_manager.py`)**  
   Manages atomic writes, serialized encrypted payloads, and SHA-256 hash integrity validation.

---

## ⚙️ Prerequisites & Dependencies

* **Python 3.8+**
* Windows (batch launch scripts provided)

### Required Libraries

```
cryptography
argon2-cffi
flask
requests
pyotp
urllib3
pyperclip
customtkinter
pillow
packaging
```

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/OmarTamer177/Vault-Guard.git
cd Vault-Guard
```

### 2. Setup Dependencies

Run the automated dependency installer (creates/uses the local virtual environment):

```cmd
install_deps.bat
```

Alternatively, manually install using `pip`:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Launch the Application

**Option A: Full GUI Suite (Recommended)**

```cmd
start_gui.bat
```
This launcher simultaneously boots:
1. The **MFA Server** (HTTPS background daemon on `127.0.0.1:5000`)
2. The **Mobile Authenticator GUI**
3. The **VaultGuard Desktop Client**

**Option B: CLI Mode**

```cmd
scripts\start_system.bat
```

---

## 🔑 First-Time Setup Walkthrough

1. **Register on Mobile Authenticator**
   - In the **VaultGuard Authenticator** window, click **Scan / Register New Device**.
   - Input your desired username (e.g., `alice`) and submit.
   - The app securely stores your secret profile locally.
2. **Retrieve your 6-digit OTP**
   - Click on your username card in the Authenticator window.
   - Note the active 6-digit code and the countdown timer.
3. **Log in to VaultGuard**
   - In the **VaultGuard Client** window:
     - Set/enter your **Master Password**.
     - Enter your **Username**.
     - Enter the current **OTP Code** from the authenticator.
   - Click **Unlock / Login**.

---

## 🔬 Testing & Verification

Comprehensive automated test suites cover cryptography, KDF parameters, TOTP synchronization, and tamper resistance:

### Run the Complete Test Suite
```cmd
run_tests.bat
```

### Run Individual Test Modules
```bash
# Cryptography tests (AES-256-GCM encryption/decryption)
python -m unittest tests.test_crypto

# Argon2id KDF verification
python -m unittest tests.test_argon2

# MFA & TOTP server/client verification
python -m unittest tests.test_mfa

# File integrity & tampering detection tests
python -m unittest tests.test_vault

# End-to-end integration workflow tests
python -m unittest tests.test_integration
```

---

## 📊 Security Specifications

| Mechanism | Standard / Parameter | Specification Detail |
|---|---|---|
| **Symmetric Encryption** | AES-256-GCM | Authenticated Encryption with Associated Data (AEAD) |
| **Key Derivation** | Argon2id | Memory: 64 MB, Iterations: 3, Parallelism: 4, Salt: 16 bytes |
| **Two-Factor Auth** | RFC 6238 TOTP | HMAC-SHA1, 6-digit token, 60s validity window |
| **Transport Layer** | TLS / HTTPS | Self-signed / adhoc SSL for local communications |
| **Integrity Check** | SHA-256 | Computed over ciphertext prior to load and verified against storage manifest |

---

## 📂 Repository Structure

```
Vault-Guard/
├── .gitignore               # Excludes bytecode, .venv, IDE, and runtime databases
├── requirements.txt         # Project dependencies
├── install_deps.bat         # Dependency installer
├── start_gui.bat            # One-click multi-process launcher
├── run_tests.bat            # Test runner
├── README.md
├── src/
│   ├── auth/
│   │   ├── mfa_server.py    # Flask HTTPS MFA server
│   │   └── mfa_client.py    # MFA client connection library
│   ├── cli/
│   │   ├── main.py          # Terminal CLI client
│   │   └── mobile_auth_app.py # Terminal authenticator simulator
│   ├── core/
│   │   ├── crypto_manager.py     # AES-GCM & Argon2id engine
│   │   ├── interfaces.py         # Abstract base classes
│   │   └── vault_file_manager.py # File storage & integrity verification
│   ├── gui/
│   │   ├── vault_gui.py          # Modern desktop vault interface
│   │   └── mobile_auth_gui.py    # Companion mobile authenticator interface
│   └── utils/
│       └── debug_env.py
├── data/
│   └── .gitkeep             # Runtime data directory (local vaults & DBs)
├── docs/
│   ├── VaultGuard_Report.tex
│   └── verification_matrix.md
├── scripts/
│   ├── run_app.bat
│   ├── start_system.bat
│   └── ...
└── tests/
    ├── test_crypto.py
    ├── test_argon2.py
    ├── test_mfa.py
    ├── test_vault.py
    └── test_integration.py
```

---

## 👥 Contributors

* **Ali Tarek** — Project Lead & Implementation
* **Omar Tamer** — Core Development & Security Features
* **Fatma Ayman** — Backend Development & MFA
* **Ahmed El-Baramouny** — Security Analysis & Testing
* **Ahmed Mohamed** — GUI Development & Documentation

---

## 📄 License & Academic Note

This project was developed for educational and demonstration purposes as part of the Information Security course.