#!/bin/bash
# Setup script for Django backend

echo "==================================="
echo "Django Backend Setup"
echo "==================================="

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || venv\Scripts\activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if not exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit .env file with your database credentials"
fi

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create admin user
echo "Creating default admin user..."
python manage.py create_admin

echo ""
echo "==================================="
echo "Setup complete!"
echo "==================================="
echo "Default admin credentials:"
echo "  Username: admin"
echo "  Password: adminpassword"
echo ""
echo "To start the server, run:"
echo "  python manage.py runserver 0.0.0.0:8000"
echo "==================================="
