#!/bin/bash
# Run Django development server

# Activate virtual environment
source venv/bin/activate || venv\Scripts\activate

# Run server on all interfaces at port 8000
python manage.py runserver 0.0.0.0:8000
