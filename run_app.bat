@echo off
set VENV_PATH=%~dp0.venv
set PYTHON="%VENV_PATH%\Scripts\python.exe"

echo [Launcher] Using Python at: %PYTHON%
echo [Launcher] Reinstalling cached pycryptodome...
%PYTHON% -m pip install pycryptodome --no-index --find-links .

echo [Launcher] Starting VaultGuard...
%PYTHON% main.py
pause
