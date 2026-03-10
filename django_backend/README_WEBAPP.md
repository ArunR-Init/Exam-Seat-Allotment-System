# 🎓 Exam Hall Allotment System - Complete Django Web Application

A comprehensive examination hall seating management system built entirely with **Django 5.0** and **Python**. This full-stack web application manages student registrations, teacher assignments, and automated seat allocations for examination halls.

---

## 🌟 Overview

This is a **complete Django web application** that serves both the backend API and frontend web pages. No separate frontend framework needed - everything is powered by Django!

### Key Highlights:
- ✅ **Pure Python/Django** - No Node.js or React required
- ✅ **Server-side rendered templates** - Fast page loads
- ✅ **Beautiful UI** - Tailwind CSS styling
- ✅ **Responsive design** - Works on all devices
- ✅ **Role-based authentication** - Students, Teachers, Admins
- ✅ **PostgreSQL database** - Reliable data storage
- ✅ **RESTful API** - Also available for programmatic access

---

## 🎯 Features

### For Students:
- 📝 **Self-Registration** - Register with roll number and details
- 🔐 **Secure Login** - Access personal dashboard
- 🎫 **View Admit Card** - See examination hall and seat number
- 👨‍🏫 **Invigilator Details** - Know who will be supervising
- 🖨️ **Print Ready** - Print admit card directly from browser

### For Teachers:
- 🔑 **Secure Access** - Login with admin-provided credentials
- 🏢 **View Assigned Hall** - See which room you're invigilating
- 📋 **Student Roster** - Complete list with seat numbers
- 🖨️ **Print List** - Print student roster for record-keeping

### For Administrators:
- 👥 **Manage Teachers** - Create teacher accounts with credentials
- 👨‍🎓 **View Students** - See all registered students
- 🎲 **Smart Allocation** - Automatically allot students to rooms
- 📊 **Dashboard** - View statistics and manage the system
- ⚙️ **Flexible Settings** - Maximum 15 students per room

---

## 🏗️ Technology Stack

**Backend:**
- **Django 5.0** - Web framework
- **PostgreSQL** - Database
- **Django REST Framework** - API endpoints
- **Python 3.10+** - Programming language

**Frontend:**
- **Django Templates** - Server-side rendering
- **Tailwind CSS** - Styling (via CDN)
- **Lucide Icons** - Beautiful icons
- **Vanilla JavaScript** - Interactive features

---

## 📁 Project Structure

```
django_backend/
├── config/                      # Main Django project configuration
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Root URL configuration
│   ├── wsgi.py                 # WSGI application
│   └── asgi.py                 # ASGI application
│
├── exam_app/                    # Main application
│   ├── models.py               # Database models (User, Room, Allotment)
│   ├── views.py                # API views (RESTful endpoints)
│   ├── template_views.py       # Template views (web pages)
│   ├── serializers.py          # DRF serializers
│   ├── urls.py                 # API URL routing
│   ├── template_urls.py        # Web page URL routing
│   ├── admin.py                # Django admin configuration
│   ├── templates/              # HTML templates
│   │   ├── base.html           # Base template with navigation
│   │   ├── home.html           # Landing page
│   │   ├── register.html       # Student registration
│   │   ├── login.html          # Login page (all roles)
│   │   ├── student_dashboard.html
│   │   ├── teacher_dashboard.html
│   │   └── admin_dashboard.html
│   └── management/
│       └── commands/
│           └── create_admin.py # Custom admin creation command
│
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
└── .env                        # Environment variables (create this)
```

---

## 🚀 Quick Start

### Prerequisites:
- Python 3.10 or higher
- PostgreSQL
- pip (Python package manager)

### Installation:

1. **Clone or navigate to the project:**
```bash
cd django_backend
```

2. **Create a `.env` file:**
```env
DB_NAME=exam_allotment
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-secret-key-here
DEBUG=True
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create database:**
```sql
CREATE DATABASE exam_allotment;
```

5. **Run migrations:**
```bash
python manage.py migrate
```

6. **Create admin user:**
```bash
python manage.py createsuperuser
```

7. **Start the server:**
```bash
python manage.py runserver
```

8. **Access the application:**
```
http://localhost:8000/
```

📖 **For detailed step-by-step instructions, see [QUICKSTART_WEBAPP.md](QUICKSTART_WEBAPP.md)**

---

## 🌐 URL Structure

### Web Pages (Template Views):
```
/                           - Home page
/register/                  - Student registration
/login/student/             - Student login
/login/teacher/             - Teacher login
/login/admin/               - Admin login
/logout/                    - Logout
/dashboard/                 - Auto-redirect to role dashboard

/student/                   - Student dashboard
/teacher/                   - Teacher dashboard
/admin-dashboard/           - Admin dashboard
/admin-dashboard/add-teacher/     - Add teacher (POST)
/admin-dashboard/allot/           - Allocate rooms (POST)
```

### API Endpoints (REST API):
```
/api/auth/register-student  - POST: Register student
/api/auth/login             - POST: Login user
/api/auth/logout            - POST: Logout user
/api/auth/me                - GET: Get current user

/api/admin/students         - GET: List all students
/api/admin/teachers         - GET: List all teachers
/api/admin/teachers         - POST: Add teacher
/api/admin/allot            - POST: Allocate rooms

/api/student/allotment      - GET: Get student's allotment
/api/teacher/room           - GET: Get teacher's room
```

---

## 💾 Database Schema

### User Model
```python
- id (Primary Key)
- username (Unique)
- name
- password (Hashed)
- role (admin / teacher / student)
```

### Room Model
```python
- id (Primary Key)
- name (e.g., "Room 1")
- teacher (Foreign Key → User)
```

### Allotment Model
```python
- id (Primary Key)
- room (Foreign Key → Room)
- student (Foreign Key → User)
- seat_number (1-15 per room)
```

---

## 🔐 Authentication

- **Session-based authentication** using Django's built-in auth system
- **Role-based access control** with three roles: admin, teacher, student
- **Password hashing** with Django's PBKDF2 algorithm
- **CSRF protection** for all forms
- **Login required decorators** for protected views

---

## 🎨 UI/UX Design

The application features a modern, clean interface built with:

- **Tailwind CSS** - Utility-first CSS framework
- **Responsive design** - Works on mobile, tablet, and desktop
- **Card-based layouts** - Clean, organized information
- **Color-coded roles:**
  - 🔵 **Blue** - Students
  - 🟣 **Indigo** - Teachers
  - ⚫ **Slate** - Admins

---

## 📊 Room Allocation Algorithm

The system uses a smart allocation algorithm:

1. **Get all students and teachers**
2. **Calculate required rooms** (15 students per room maximum)
3. **Validate teacher availability** (need 1 teacher per room)
4. **Shuffle students randomly** for fair distribution
5. **Create rooms** with sequential naming (Room 1, Room 2, etc.)
6. **Assign students** with seat numbers 1-15
7. **Assign one teacher** per room as invigilator

**Example:**
- 45 students → 3 rooms needed
- Room 1: 15 students (seats 1-15) + Teacher A
- Room 2: 15 students (seats 1-15) + Teacher B
- Room 3: 15 students (seats 1-15) + Teacher C

---

## 🧪 Testing

### Manual Testing Steps:

1. **Test Student Registration:**
   - Go to `/register/`
   - Register with roll number, name, password
   - Verify auto-login and redirect

2. **Test Admin Functions:**
   - Login as admin at `/login/admin/`
   - Add 3 teachers
   - Register 30 students
   - Click "Allot Rooms"
   - Verify 2 rooms created

3. **Test Student Dashboard:**
   - Login as student
   - Click "Reveal My Allotment"
   - Verify room name and seat number displayed

4. **Test Teacher Dashboard:**
   - Login as teacher
   - Click "Reveal Assignment"
   - Verify room and student list displayed

---

## 🚀 Deployment

**For Production Deployment:**

1. Set environment variables:
```env
DEBUG=False
SECRET_KEY=<strong-secret-key>
ALLOWED_HOSTS=yourdomain.com
```

2. Collect static files:
```bash
python manage.py collectstatic
```

3. Use a production server (Gunicorn):
```bash
pip install gunicorn
gunicorn config.wsgi:application
```

4. Set up a reverse proxy (Nginx)
5. Use a production database with proper credentials
6. Enable HTTPS with SSL certificate

---

## 📝 Development Notes

### Custom User Model:
The project uses a custom User model (`exam_app.User`) instead of Django's default. This provides:
- Custom fields (name, role)
- Role-based permissions
- Flexible authentication

### Session vs Token Auth:
- Web pages use Django session authentication
- API endpoints support both sessions and can be extended with tokens
- CORS is configured for API access

### Template Context:
All templates have access to:
- `user` - Current logged-in user
- `request` - HTTP request object
- `messages` - Django messages framework

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

---

## 📄 License

This project is open source and available under the MIT License.

---

## 📧 Support

For issues, questions, or suggestions:
- Create an issue in the repository
- Check existing documentation
- Review the QUICKSTART guide

---

## 🎓 Use Cases

This system is perfect for:
- **Universities** - Manage semester exams
- **Schools** - Conduct annual examinations
- **Training Centers** - Organize certification exams
- **Competition Organizers** - Seat allocation for contests

---

## 🔄 Future Enhancements

Potential improvements:
- [ ] Email notifications for allotments
- [ ] PDF generation for admit cards
- [ ] Exam schedule management
- [ ] Multiple exam sessions
- [ ] Room capacity customization
- [ ] Student search and filtering
- [ ] Export to Excel
- [ ] Real-time updates with WebSockets

---

## 👏 Acknowledgments

- **Django** - Excellent web framework
- **Tailwind CSS** - Beautiful styling
- **Lucide** - Clean icons
- **PostgreSQL** - Reliable database

---

**Built with ❤️ using Django and Python**

**🎉 Start managing your examinations efficiently today!**

---

## 📚 Additional Documentation

- [QUICKSTART_WEBAPP.md](QUICKSTART_WEBAPP.md) - Detailed setup guide
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - REST API reference
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Technical overview
- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) - Migration from Node.js

---

*Last Updated: 2026*
