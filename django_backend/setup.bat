@echo off
REM Setup script for Django backend (Windows)

echo ===================================
echo Django Backend Setup
echo ===================================

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if not exists
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo Please edit .env file with your database credentials
)

REM Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Create admin user
echo Creating default admin user...
python manage.py create_admin

echo.
echo ===================================
echo Setup complete!
echo ===================================
echo Default admin credentials:
echo   Username: admin
echo   Password: adminpassword
echo.
echo To start the server, run:
echo   python manage.py runserver 0.0.0.0:8000
echo ===================================
pause
