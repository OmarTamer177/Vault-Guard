@echo off
set VENV_PATH=%~dp0.venv
set PYTHON="%VENV_PATH%\Scripts\python.exe"

echo [Fixer] Using Python at: %PYTHON%

echo [Fixer] Uninstalling conflicting packages...
%PYTHON% -m pip uninstall -y crypto pycrypto pycryptodome

echo [Fixer] Installing correct pycryptodome...
%PYTHON% -m pip install pycryptodome flask pyotp requests pyopenssl

echo [Fixer] Verifying installation...
%PYTHON% -c "from Crypto.Protocol.KDF import Argon2; print('SUCCESS: Argon2 found.')"

if %errorlevel% neq 0 (
    echo [ERROR] Fix failed. Argon2 still missing.
    pause
    exit /b 1
)

echo [Fixer] Success! Starting App...
%PYTHON% main.py
pause
