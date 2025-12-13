@echo off
cd /d "%~dp0"
echo [Migration] Uninstalling legacy packages...
"%~dp0.venv\Scripts\python.exe" -m pip uninstall -y crypto pycrypto pycryptodome

echo [Migration] Installing pycryptodomex...
"%~dp0.venv\Scripts\python.exe" -m pip install pycryptodomex

echo [Migration] Done.
pause
