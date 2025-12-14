@echo off
echo ========================================================
echo  HealFlow Hospital Management System - Quick Start
echo ========================================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Check if database exists
if not exist "instance\hospital.db" (
    echo Database not found. Seeding database...
    python seed_data.py
) else (
    echo Database already exists
)

echo.
echo Starting HealFlow...
echo.
echo Access the application at:
echo    Local: http://127.0.0.1:5000
echo.
echo Default login:
echo    Admin: admin / admin123
echo    Doctor: dr.smith / doctor123
echo    Patient: john.doe / patient123
echo.
echo Press Ctrl+C to stop the server
echo ========================================================
echo.

python app.py
pause
