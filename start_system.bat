@echo off
set VENV_PATH=%~dp0.venv
set PYTHON="%VENV_PATH%\Scripts\python.exe"

echo [System] Launching MFA Server...
start "MFA Server (Do Not Close)" %PYTHON% mfa_server.py

echo [System] Launching Mobile App Simulator...
start "Mobile App" %PYTHON% mobile_auth_app.py

echo [System] Waiting 5 seconds for server to start...
timeout /t 5 > NUL

echo [System] Launching VaultGuard Client...
%PYTHON% main.py
pause
