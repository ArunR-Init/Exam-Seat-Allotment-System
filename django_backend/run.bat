@echo off
REM Run Django development server (Windows)

REM Activate virtual environment
call venv\Scripts\activate

REM Run server on all interfaces at port 8000
python manage.py runserver 0.0.0.0:8000
