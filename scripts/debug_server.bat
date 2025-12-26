@echo off
set VENV_PATH=%~dp0.venv
set PYTHON="%VENV_PATH%\Scripts\python.exe"

echo [Debug] Starting MFA Server...
%PYTHON% mfa_server.py
echo.
echo [Debug] Server process ended. If you see an error above, paste it to the chat.
pause
