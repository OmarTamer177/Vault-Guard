@echo off
set VENV_PATH=c:\Users\aliab\Desktop\Semester 9\Computer Networks and Security\VaultGuard_Project\.venv
echo Activating venv...
call "%VENV_PATH%\Scripts\activate.bat"
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
echo Done.
