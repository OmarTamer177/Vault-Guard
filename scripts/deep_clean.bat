@echo off
cd /d "%~dp0.."
set "SITE_PACKAGES=%CD%\.venv\Lib\site-packages"

echo [Deep Clean] Target: "%SITE_PACKAGES%"

if exist "%SITE_PACKAGES%\Crypto" (
    echo Removes existing Crypto folder...
    rmdir /s /q "%SITE_PACKAGES%\Crypto"
)

echo Cleaning metadata...
if exist "%SITE_PACKAGES%" (
    pushd "%SITE_PACKAGES%"
    if exist "pycryptodome*" for /d %%p in (pycryptodome*) do rmdir /s /q "%%p"
    if exist "crypto-*" for /d %%p in (crypto-*) do rmdir /s /q "%%p"
    if exist "pycrypto-*" for /d %%p in (pycrypto-*) do rmdir /s /q "%%p"
    popd
)

echo Re-installing pycryptodome...
"%CD%\.venv\Scripts\python.exe" -m pip install pycryptodome==3.23.0

echo Verification...
"%CD%\.venv\Scripts\python.exe" -c "from Crypto.Protocol.KDF import Argon2; print('SUCCESS: Argon2 is working.')"

echo.
echo If SUCCESS is printed above, you are good to go.
pause
