# Django Backend - Exam Allotment System

This is a complete Django conversion of the original Node.js/Express backend. All functionality, logic, validations, and edge cases have been preserved exactly as in the original implementation.

## Overview

The Django backend replicates the exact behavior of the Node.js backend using:
- **Django 5.0** - Web framework
- **Django REST Framework** - API endpoints
- **PostgreSQL** - Database (same as original)
- **Session-based authentication** - Matching Express sessions

## Project Structure

```
django_backend/
├── config/                    # Django project configuration
│   ├── __init__.py
│   ├── settings.py           # Main settings file
│   ├── urls.py               # Root URL configuration
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
├── exam_app/                  # Main application
│   ├── management/
│   │   └── commands/
│   │       └── create_admin.py  # Command to create default admin
│   ├── __init__.py
│   ├── models.py             # Database models (User, Room, Allotment)
│   ├── views.py              # API views/endpoints
│   ├── serializers.py        # Data validation (like Zod schemas)
│   ├── urls.py               # App URL configuration
│   ├── admin.py              # Django admin configuration
│   ├── apps.py               # App configuration
│   └── tests.py              # Test cases
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore file
├── setup.sh / setup.bat      # Setup scripts
├── run.sh / run.bat          # Run scripts
└── README.md                 # This file
```

## Features Implemented

### Authentication System
- ✅ Student registration with validation
- ✅ Login for admin/teacher/student with role-based access
- ✅ Session-based authentication
- ✅ Logout functionality
- ✅ Current user endpoint (`/api/auth/me`)

### Admin Features
- ✅ View all students
- ✅ View all teachers
- ✅ Add new teachers
- ✅ Auto-allot students to rooms
  - Automatically creates rooms (max 15 students per room)
  - Randomly shuffles students
  - Validates sufficient teachers available
  - Clears old allotments before creating new ones

### Teacher Features
- ✅ View assigned room
- ✅ View all students in their room with seat numbers

### Student Features
- ✅ View room allotment details
- ✅ View seat number

## API Endpoints

All endpoints match the original Node.js implementation:

### Authentication
- `POST /api/auth/register-student` - Register a new student
- `POST /api/auth/login` - Login (admin/teacher/student)
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user

### Admin (requires admin role)
- `GET /api/admin/students` - Get all students
- `GET /api/admin/teachers` - Get all teachers
- `POST /api/admin/teachers` - Add a new teacher
- `POST /api/admin/allot` - Auto-allot students to rooms

### Student (requires student role)
- `GET /api/student/allotment` - Get room allotment

### Teacher (requires teacher role)
- `GET /api/teacher/room` - Get assigned room and students

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- PostgreSQL database
- pip (Python package manager)

### Quick Setup

#### On Windows:
```bash
# Run the setup script
setup.bat

# Or manually:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your database credentials
python manage.py makemigrations
python manage.py migrate
python manage.py create_admin
```

#### On Linux/Mac:
```bash
# Make scripts executable
chmod +x setup.sh run.sh

# Run the setup script
./setup.sh

# Or manually:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database credentials
python manage.py makemigrations
python manage.py migrate
python manage.py create_admin
```

### Environment Configuration

Edit the `.env` file with your database credentials:

```env
DB_NAME=exam_allotment
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5000
```

## Running the Server

### Using Scripts:

#### Windows:
```bash
run.bat
```

#### Linux/Mac:
```bash
./run.sh
```

### Manually:
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Run server
python manage.py runserver 0.0.0.0:8000
```

The server will start at `http://localhost:8000`

## Default Credentials

After setup, the following admin account is created:

- **Username:** `admin`
- **Password:** `adminpassword`

**Important:** Change the admin password in production!

## Database Schema

### Users Table
- `id` - Primary key (auto-increment)
- `username` - Unique username/roll number
- `name` - Full name
- `password` - Hashed password
- `role` - Role (admin/teacher/student)

### Rooms Table
- `id` - Primary key (auto-increment)
- `name` - Room name
- `teacher_id` - Foreign key to Users (teacher)

### Allotments Table
- `id` - Primary key (auto-increment)
- `student_id` - Foreign key to Users (student)
- `room_id` - Foreign key to Rooms
- `seat_number` - Seat number in room

## Key Differences from Node.js Version

While the functionality is identical, here are the technical differences:

1. **Framework**: Django instead of Express
2. **ORM**: Django ORM instead of Drizzle
3. **Validation**: Django REST Framework serializers instead of Zod
4. **Sessions**: Django sessions instead of Express sessions
5. **Admin Interface**: Built-in Django admin panel available at `/admin/`

## Validations & Edge Cases

All validations from the original are implemented:

✅ Username uniqueness validation  
✅ Password confirmation matching  
✅ Role-based access control  
✅ Required field validations  
✅ Insufficient teachers check before allotment  
✅ Empty student list check  
✅ Invalid credentials handling  
✅ Session management  

## Testing the API

### Using curl:

```bash
# Register a student
curl -X POST http://localhost:8000/api/auth/register-student \
  -H "Content-Type: application/json" \
  -d '{"username":"S001","name":"John Doe","password":"pass123","confirmPassword":"pass123"}' \
  -c cookies.txt

# Login as admin
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"adminpassword","role":"admin"}' \
  -c cookies.txt

# Get current user
curl -X GET http://localhost:8000/api/auth/me \
  -b cookies.txt

# Get all students (admin only)
curl -X GET http://localhost:8000/api/admin/students \
  -b cookies.txt
```

## Development Tools

### Django Admin Panel
Access the admin panel at `http://localhost:8000/admin/` using superuser credentials.

### Database Management
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell
```

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Configure proper `SECRET_KEY`
3. Set appropriate `ALLOWED_HOSTS`
4. Use a proper WSGI server (gunicorn is included in requirements)
5. Set up static files serving
6. Use a production database with proper credentials
7. Enable HTTPS and set `SESSION_COOKIE_SECURE=True`

### Example Production Start:
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

## Integration with Frontend

The frontend (React/Vite) **remains unchanged**. Update the API base URL if needed.

The Django backend maintains the same API contract:
- Same endpoints
- Same request/response formats
- Same session-based authentication
- Same error handling

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Verify database credentials in `.env`
- Check if database exists: `psql -U postgres -l`

### Port Already in Use
```bash
# Use a different port
python manage.py runserver 0.0.0.0:8001
```

### CORS Errors
- Check `CORS_ALLOWED_ORIGINS` in `.env`
- Ensure frontend URL is included

### Migration Issues
```bash
# Reset migrations (WARNING: deletes data)
python manage.py migrate exam_app zero
python manage.py makemigrations
python manage.py migrate
```

## Support & Maintenance

The Django implementation maintains 100% functional parity with the original Node.js version. All business logic, validations, and edge cases have been preserved.

## License

Same as the original project.
