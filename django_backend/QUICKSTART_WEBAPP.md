# Complete Django Web Application - Quick Start Guide

This guide will help you set up and run the **Exam Hall Allotment System** as a complete Django web application. The system now serves both the backend API AND the frontend web pages, making it a pure Python/Django solution.

---

## 📋 What's New?

This is now a **complete Django web application** with:
- Django serving HTML pages (no React/Vite needed)
- Server-side rendered templates with Tailwind CSS
- Django handling both frontend AND backend
- Pure Python/Django codebase

---

## 🚀 Prerequisites

Before you begin, ensure you have:

1. **Python 3.10+** installed ([Download](https://www.python.org/downloads/))
2. **PostgreSQL** installed and running ([Download](https://www.postgresql.org/download/))
3. **pip** (Python package manager - comes with Python)

---

## 📦 Step 1: Create PostgreSQL Database

Open your PostgreSQL terminal (psql) or pgAdmin and run:

```sql
CREATE DATABASE exam_allotment;
```

Or use the command line:

```bash
# Windows (Command Prompt)
psql -U postgres -c "CREATE DATABASE exam_allotment;"

# Linux/Mac
sudo -u postgres psql -c "CREATE DATABASE exam_allotment;"
```

---

## 🔧 Step 2: Configure Environment Variables

Navigate to the `django_backend` folder:

```bash
cd django_backend
```

Create a `.env` file (or edit if it exists):

```env
# Database Configuration
DB_NAME=exam_allotment
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432

# Django Configuration
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# For production, set DEBUG=False and use a strong SECRET_KEY
```

**Important:** Replace `your_password_here` with your actual PostgreSQL password!

---

## 📥 Step 3: Install Python Dependencies

Make sure you're in the `django_backend` folder, then install dependencies:

```bash
# Install all required packages
pip install -r requirements.txt
```

This will install:
- Django 5.0
- psycopg2 (PostgreSQL adapter)
- djangorestframework (for API endpoints)
- python-dotenv (for environment variables)

---

## 🗄️ Step 4: Run Database Migrations

Apply the database schema:

```bash
python manage.py migrate
```

This creates all necessary tables (users, rooms, allotments, etc.)

---

## 👤 Step 5: Create Admin User

Create a superuser account for the admin dashboard:

```bash
python manage.py createsuperuser
```

Follow the prompts:
- **Username:** Choose an admin username (e.g., `admin`)
- **Name:** Your full name (e.g., `System Admin`)
- **Password:** Choose a secure password
- **Role:** Enter `admin`

**Note:** The role MUST be `admin` for admin access!

---

## ▶️ Step 6: Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

You should see:

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## 🌐 Step 7: Access the Application

**Open your web browser** and navigate to:

```
http://localhost:8000/
```

You'll see the home page with three cards for Students, Teachers, and Admin!

### Available Pages:

- **Home:** http://localhost:8000/
- **Student Registration:** http://localhost:8000/register/
- **Student Login:** http://localhost:8000/login/student/
- **Teacher Login:** http://localhost:8000/login/teacher/
- **Admin Login:** http://localhost:8000/login/admin/
- **Admin Dashboard:** http://localhost:8000/admin-dashboard/
- **Student Dashboard:** http://localhost:8000/student/
- **Teacher Dashboard:** http://localhost:8000/teacher/

---

## 🎯 Step 8: Test the Application

### 1. Login as Admin

1. Go to: http://localhost:8000/login/admin/
2. Enter the credentials you created in Step 5
3. You'll be redirected to the Admin Dashboard

### 2. Add Teachers

1. In the Admin Dashboard, click on the **Teachers** tab
2. Click **Add Teacher** button
3. Fill in:
   - Name: `Dr. John Smith`
   - Username: `jsmith`
   - Password: `teacher123`
4. Click **Save Teacher**
5. Add at least 1-2 more teachers

### 3. Register Students

1. Logout and go to: http://localhost:8000/register/
2. Register a student:
   - Roll Number: `2021001`
   - Full Name: `Alice Johnson`
   - Password: `student123`
3. Register several more students (at least 5-10)

### 4. Allocate Rooms

1. Login as Admin again
2. Go to the **Students** tab in Admin Dashboard
3. Click **Allot Rooms** button
4. Confirmation: Click OK
5. You'll see: "Allocation successful! Created X rooms and allotted Y students."

### 5. View Student Allotment

1. Login as a student: http://localhost:8000/login/student/
2. Use credentials: `2021001` / `student123`
3. Click **Reveal My Allotment**
4. You'll see the exam hall name, seat number, and invigilator details

### 6. View Teacher Room

1. Login as a teacher: http://localhost:8000/login/teacher/
2. Use credentials: `jsmith` / `teacher123`
3. Click **Reveal Assignment**
4. You'll see the room name and list of students

---

## 🎨 Features

### Student Features:
- Self-registration with roll number
- Login with roll number and password
- View assigned examination hall
- View seat number
- View invigilator details
- Print admit card

### Teacher Features:
- Login with username and password
- View assigned examination hall
- View complete student roster with seat numbers
- Print student list

### Admin Features:
- Add teachers with credentials
- View all registered students
- View all registered teachers
- Allocate students to rooms (max 15 per room)
- Automatic room creation with teacher assignment
- View statistics (students count, teachers count, rooms count)

---

## 🔒 Authentication & Security

- **Role-based access control:** Students, Teachers, and Admin have separate dashboards
- **Password hashing:** All passwords are securely hashed using Django's built-in system
- **Session management:** User sessions are managed securely with Django sessions
- **CSRF protection:** All forms are protected against CSRF attacks
- **Login required:** Dashboards require authentication

---

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones

All pages use Tailwind CSS for beautiful, modern UI design!

---

## 🛠️ Troubleshooting

### Database Connection Error

**Error:** `django.db.utils.OperationalError: could not connect to server`

**Solution:**
1. Make sure PostgreSQL is running
2. Verify your `.env` file has correct database credentials
3. Check if the database `exam_allotment` exists

### Port Already in Use

**Error:** `Error: That port is already in use.`

**Solution:**
Run on a different port:
```bash
python manage.py runserver 8001
```

### Module Not Found Error

**Error:** `ModuleNotFoundError: No module named 'django'`

**Solution:**
Install dependencies:
```bash
pip install -r requirements.txt
```

### Admin Login Not Working

**Error:** Admin credentials not working

**Solution:**
Make sure you created the superuser with role `admin`:
```bash
python manage.py createsuperuser
```
Enter `admin` when prompted for role.

---

## 📚 Additional Resources

- **Django Documentation:** https://docs.djangoproject.com/
- **Tailwind CSS:** https://tailwindcss.com/docs
- **PostgreSQL Documentation:** https://www.postgresql.org/docs/

---

## 🎉 You're All Set!

Your Exam Hall Allotment System is now running! Enjoy using the application.

For production deployment, see `DEPLOYMENT.md` (coming soon).

**Need help?** Check the `README.md` for more detailed information.

---

## 🔄 Quick Reference Commands

```bash
# Navigate to project
cd django_backend

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start server
python manage.py runserver

# Create a backup of database
python manage.py dumpdata > backup.json

# Load data from backup
python manage.py loaddata backup.json
```

---

**🎓 Happy Exam Management!**
