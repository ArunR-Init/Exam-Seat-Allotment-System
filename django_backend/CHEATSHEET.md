# Django Backend - Quick Reference Cheat Sheet

Fast reference for common operations and commands.

---

## 🚀 Quick Start (Copy & Paste)

### Windows Setup
```cmd
cd django_backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
REM Edit .env with your database credentials
python manage.py migrate
python manage.py create_admin
python manage.py runserver 0.0.0.0:8000
```

### Linux/Mac Setup
```bash
cd django_backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database credentials
python manage.py migrate
python manage.py create_admin
python manage.py runserver 0.0.0.0:8000
```

---

## 🔑 Default Credentials

```
Username: admin
Password: adminpassword
Role: admin
```

---

## 📡 API Endpoints

### Authentication
```bash
# Register Student
POST /api/auth/register-student
Body: {"username":"S001","name":"John Doe","password":"pass","confirmPassword":"pass"}

# Login
POST /api/auth/login
Body: {"username":"admin","password":"adminpassword","role":"admin"}

# Logout
POST /api/auth/logout

# Get Current User
GET /api/auth/me
```

### Admin (requires admin login)
```bash
# Get All Students
GET /api/admin/students

# Get All Teachers
GET /api/admin/teachers

# Add Teacher
POST /api/admin/teachers
Body: {"username":"T001","name":"Dr. Smith","password":"teacher123"}

# Auto-Allot Rooms
POST /api/admin/allot
```

### Student (requires student login)
```bash
# Get Allotment
GET /api/student/allotment
```

### Teacher (requires teacher login)
```bash
# Get Room & Students
GET /api/teacher/room
```

---

## 💻 Django Management Commands

### Database
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (WARNING: deletes all data)
python manage.py flush

# Django shell
python manage.py shell
```

### Users
```bash
# Create admin user (custom command)
python manage.py create_admin

# Create superuser (Django admin panel)
python manage.py createsuperuser
```

### Server
```bash
# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8001

# Run on all interfaces
python manage.py runserver 0.0.0.0:8000
```

### Other
```bash
# Check for issues
python manage.py check

# Collect static files (production)
python manage.py collectstatic
```

---

## 🧪 Testing with curl

### Save Cookies (Important!)
```bash
# Set cookie file
COOKIES="cookies.txt"

# Use -c to save cookies (login)
# Use -b to send cookies (authenticated requests)
```

### Complete Flow
```bash
# 1. Register Student
curl -X POST http://localhost:8000/api/auth/register-student \
  -H "Content-Type: application/json" \
  -d '{"username":"S001","name":"John","password":"pass","confirmPassword":"pass"}' \
  -c cookies.txt

# 2. Login as Admin
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"adminpassword","role":"admin"}' \
  -c cookies.txt

# 3. Get Current User
curl http://localhost:8000/api/auth/me -b cookies.txt

# 4. Get Students
curl http://localhost:8000/api/admin/students -b cookies.txt

# 5. Add Teacher
curl -X POST http://localhost:8000/api/admin/teachers \
  -H "Content-Type: application/json" \
  -d '{"username":"T001","name":"Dr. Smith","password":"teacher123"}' \
  -b cookies.txt

# 6. Allot Rooms
curl -X POST http://localhost:8000/api/admin/allot -b cookies.txt

# 7. Logout
curl -X POST http://localhost:8000/api/auth/logout -b cookies.txt
```

---

## 🔧 Environment Variables (.env)

```env
# Database
DB_NAME=exam_allotment
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS (comma-separated)
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5000

# CSRF (comma-separated)
CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://localhost:5000
```

---

## 🐛 Common Issues & Quick Fixes

### Database Connection Error
```bash
# Check PostgreSQL is running
psql -U postgres -l

# Check .env file exists and has correct credentials
cat .env
```

### Port Already in Use
```bash
# Use different port
python manage.py runserver 8001

# Or kill process using port 8000 (Linux/Mac)
lsof -ti:8000 | xargs kill -9

# Or kill process using port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### CORS Errors
```bash
# Add frontend URL to .env
CORS_ALLOWED_ORIGINS=http://localhost:5173,...

# Restart server
```

### Migration Issues
```bash
# Delete migrations and recreate
rm exam_app/migrations/00*.py
python manage.py makemigrations
python manage.py migrate
```

### Admin Login Not Working
```bash
# Recreate admin user
python manage.py create_admin
```

---

## 📁 Important File Locations

```
django_backend/
├── config/settings.py          ← Django settings
├── exam_app/models.py          ← Database models
├── exam_app/views.py           ← API logic
├── exam_app/serializers.py     ← Validation
├── .env                        ← Your config (create from .env.example)
└── manage.py                   ← Django CLI
```

---

## 🌐 URLs

```
API Base:      http://localhost:8000/api
Admin Panel:   http://localhost:8000/admin/
Health Check:  http://localhost:8000/api/auth/me
```

---

## 📊 Database Quick Access

### PostgreSQL CLI
```bash
# Connect to database
psql -U postgres -d exam_allotment

# List tables
\dt

# View users
SELECT * FROM users;

# View rooms
SELECT * FROM rooms;

# View allotments
SELECT * FROM allotments;

# Exit
\q
```

### Django Shell
```python
# Start shell
python manage.py shell

# Import models
from exam_app.models import User, Room, Allotment

# Get all users
User.objects.all()

# Get admin user
User.objects.get(username='admin')

# Get all students
User.objects.filter(role='student')

# Count students
User.objects.filter(role='student').count()

# Exit
exit()
```

---

## 🔐 Security Checklist (Production)

```bash
# 1. Change DEBUG to False
DEBUG=False

# 2. Set proper SECRET_KEY
SECRET_KEY=<generate-random-key>

# 3. Set ALLOWED_HOSTS
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# 4. Enable HTTPS cookies
SESSION_COOKIE_SECURE=True

# 5. Set proper CORS origins
CORS_ALLOWED_ORIGINS=https://yourdomain.com

# 6. Change admin password
python manage.py shell
>>> from exam_app.models import User
>>> admin = User.objects.get(username='admin')
>>> admin.set_password('new-secure-password')
>>> admin.save()
```

---

## 🚀 Production Deployment

### Using Gunicorn
```bash
# Install gunicorn (already in requirements.txt)
pip install gunicorn

# Run production server
gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --timeout 60 \
  --access-logfile - \
  --error-logfile -
```

### Using systemd (Linux)
```bash
# Create service file: /etc/systemd/system/django-backend.service
[Unit]
Description=Django Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/django_backend
ExecStart=/path/to/venv/bin/gunicorn config.wsgi:application --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable django-backend
sudo systemctl start django-backend
sudo systemctl status django-backend
```

---

## 📦 Dependency Management

```bash
# Install dependencies
pip install -r requirements.txt

# Update dependencies
pip install --upgrade -r requirements.txt

# Add new dependency
pip install package-name
pip freeze > requirements.txt

# Check outdated packages
pip list --outdated
```

---

## 🧪 Test Automation

```bash
# Run automated test suite
python test_backend.py

# Expected output:
# ✅ Passed: 17
# ❌ Failed: 0
# 📊 Total: 17
# 📈 Success Rate: 100%
```

---

## 📝 Quick Python Snippets

### Create Test User
```python
from exam_app.models import User

# Create student
student = User.objects.create_user(
    username='S001',
    password='password123',
    name='Test Student',
    role='student'
)

# Create teacher
teacher = User.objects.create_user(
    username='T001',
    password='password123',
    name='Test Teacher',
    role='teacher'
)
```

### Create Test Data
```python
from exam_app.models import User, Room, Allotment

# Create 10 students
for i in range(1, 11):
    User.objects.create_user(
        username=f'S{i:03d}',
        password='password123',
        name=f'Student {i}',
        role='student'
    )

# Create 2 teachers
for i in range(1, 3):
    User.objects.create_user(
        username=f'T{i:03d}',
        password='password123',
        name=f'Teacher {i}',
        role='teacher'
    )
```

---

## 📚 Documentation Quick Links

| Document | Purpose |
|----------|---------|
| [INDEX.md](INDEX.md) | Start here - navigation hub |
| [QUICKSTART.md](QUICKSTART.md) | 5-minute setup |
| [README.md](README.md) | Complete guide |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | All endpoints |
| [FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md) | Frontend setup |

---

## 💡 Pro Tips

1. **Always activate venv** before running commands
   ```bash
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. **Use cookies** with curl for authenticated requests
   ```bash
   -c cookies.txt  # Save cookies
   -b cookies.txt  # Send cookies
   ```

3. **Check server logs** in terminal for errors

4. **Use Django shell** for quick database queries
   ```bash
   python manage.py shell
   ```

5. **Test API** with curl before integrating frontend

6. **Read INDEX.md** first for navigation

---

## ✅ Pre-Flight Checklist

Before running the server:
- [ ] PostgreSQL is running
- [ ] `.env` file exists with correct credentials
- [ ] Virtual environment is activated
- [ ] Dependencies are installed (`pip install -r requirements.txt`)
- [ ] Migrations are applied (`python manage.py migrate`)
- [ ] Admin user is created (`python manage.py create_admin`)

---

## 🎯 Most Used Commands

```bash
# Setup (one-time)
./setup.sh  # or setup.bat

# Run server
python manage.py runserver 0.0.0.0:8000

# Test API
curl http://localhost:8000/api/auth/me

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Django shell
python manage.py shell

# Run tests
python test_backend.py
```

---

## 📞 Getting Help

1. Check this cheat sheet first
2. Read [INDEX.md](INDEX.md) for documentation links
3. Check error logs in terminal
4. Test with curl to isolate issues
5. Review `.env` configuration
6. Check PostgreSQL is running

---

**Keep this file handy for quick reference! 📌**
