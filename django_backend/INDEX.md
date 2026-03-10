# Django Backend - Complete Documentation Index

Welcome to the Django backend documentation for the Exam Allotment System!

---

## 📚 Documentation Overview

This Django project is a complete conversion of the original Node.js/Express backend. All functionality has been preserved with 100% parity.

### Quick Links

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **[QUICKSTART.md](QUICKSTART.md)** | Get running in 5 minutes | Start here! |
| **[README.md](README.md)** | Complete setup & features | After quick start |
| **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** | All API endpoints | For frontend integration |
| **[FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md)** | Connect frontend to backend | When integrating with React app |
| **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** | Node.js to Django comparison | For understanding the conversion |
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | Complete project overview | For comprehensive understanding |

---

## 🚀 Getting Started (Fastest Path)

### 1. Quick Setup (5 minutes)
```bash
cd django_backend
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac
pip install -r requirements.txt
cp .env.example .env           # Edit with your DB credentials
python manage.py migrate
python manage.py create_admin
python manage.py runserver 0.0.0.0:8000
```

**Default Login**: `admin` / `adminpassword`

### 2. Test API (1 minute)
```bash
curl http://localhost:8000/api/auth/me
```

### 3. Connect Frontend (2 minutes)
Update API URL in your frontend:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

**Done!** ✅

---

## 📖 Documentation by Use Case

### I want to...

#### ...get the backend running quickly
→ Read: **[QUICKSTART.md](QUICKSTART.md)**

#### ...understand all features and setup
→ Read: **[README.md](README.md)**

#### ...integrate with my frontend
→ Read: **[FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md)**

#### ...know all API endpoints
→ Read: **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)**

#### ...understand the Node.js to Django conversion
→ Read: **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)**

#### ...get a complete project overview
→ Read: **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**

---

## 🎯 Key Features

### Authentication & Authorization ✅
- Student self-registration
- Role-based login (admin/teacher/student)
- Session-based authentication
- Password hashing (PBKDF2)

### Admin Features ✅
- View all students and teachers
- Add new teachers
- Auto-allot students to rooms
- Room allotment algorithm (max 15 per room)

### Student Features ✅
- View room allotment
- View seat number
- Self-registration

### Teacher Features ✅
- View assigned room
- View all students in room
- See seat assignments

---

## 🛠️ Tech Stack

- **Framework**: Django 5.0
- **API**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: Django Sessions
- **Validation**: DRF Serializers
- **Python**: 3.10+

---

## 📁 Project Structure

```
django_backend/
├── 📄 Documentation
│   ├── README.md                    ← Main documentation
│   ├── QUICKSTART.md                ← 5-minute setup guide
│   ├── API_DOCUMENTATION.md         ← All endpoints reference
│   ├── FRONTEND_INTEGRATION.md      ← Frontend connection guide
│   ├── MIGRATION_GUIDE.md           ← Node.js comparison
│   ├── PROJECT_SUMMARY.md           ← Complete overview
│   └── INDEX.md                     ← This file
│
├── 🔧 Configuration
│   ├── config/                      ← Django settings
│   │   ├── settings.py              ← Main settings
│   │   ├── urls.py                  ← URL routing
│   │   └── wsgi.py / asgi.py        ← Server entry points
│   ├── .env.example                 ← Environment variables template
│   ├── .gitignore                   ← Git ignore rules
│   └── requirements.txt             ← Python dependencies
│
├── 📦 Application
│   └── exam_app/                    ← Main app
│       ├── models.py                ← Database models
│       ├── views.py                 ← API endpoints
│       ├── serializers.py           ← Data validation
│       ├── urls.py                  ← App routing
│       ├── admin.py                 ← Admin panel config
│       └── management/              ← Management commands
│           └── commands/
│               └── create_admin.py  ← Admin creation
│
├── 🚀 Scripts
│   ├── setup.sh / setup.bat         ← Automated setup
│   ├── run.sh / run.bat             ← Run server
│   └── manage.py                    ← Django CLI
│
└── 📊 Database
    └── (PostgreSQL - external)
```

---

## 🔑 Default Credentials

After setup, use these credentials:

- **Username**: `admin`
- **Password**: `adminpassword`
- **Role**: admin

⚠️ **Change in production!**

---

## 🌐 API Endpoints Summary

### Authentication
- `POST /api/auth/register-student` - Register student
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user

### Admin (requires admin role)
- `GET /api/admin/students` - List students
- `GET /api/admin/teachers` - List teachers
- `POST /api/admin/teachers` - Add teacher
- `POST /api/admin/allot` - Allot rooms

### Student (requires student role)
- `GET /api/student/allotment` - View allotment

### Teacher (requires teacher role)
- `GET /api/teacher/room` - View room & students

**Complete details**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## 🧪 Testing

### Quick Test
```bash
# Get current user (should return null)
curl http://localhost:8000/api/auth/me

# Login as admin
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"adminpassword","role":"admin"}' \
  -c cookies.txt

# Get current user (should return admin)
curl http://localhost:8000/api/auth/me -b cookies.txt
```

### Full Testing
See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete test examples.

---

## 🐛 Troubleshooting

### Common Issues

**Database connection failed**
→ Check PostgreSQL is running and `.env` has correct credentials

**Port already in use**
→ Use different port: `python manage.py runserver 0.0.0.0:8001`

**CORS errors in frontend**
→ Add frontend URL to `CORS_ALLOWED_ORIGINS` in `.env`

**Cookies not working**
→ Ensure `credentials: 'include'` in frontend fetch/axios

**More help**: See [README.md](README.md) troubleshooting section

---

## 🚢 Deployment

### Development
```bash
python manage.py runserver 0.0.0.0:8000
```

### Production
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

**Important**: Set `DEBUG=False` and configure proper `SECRET_KEY` in production!

---

## 📚 Learning Path

### For New Django Developers
1. Read [QUICKSTART.md](QUICKSTART.md) to get running
2. Explore Django admin at `/admin/`
3. Read [README.md](README.md) to understand features
4. Study `models.py` to see database schema
5. Study `views.py` to see API logic
6. Read [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for Node.js comparison

### For Experienced Django Developers
1. Skim [README.md](README.md) for project overview
2. Check `models.py` for schema
3. Check `views.py` for business logic
4. Check `serializers.py` for validation
5. Review `settings.py` for configuration

### For Frontend Developers
1. Read [QUICKSTART.md](QUICKSTART.md) to setup backend
2. Read [FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md) for integration
3. Use [API_DOCUMENTATION.md](API_DOCUMENTATION.md) as reference
4. Test endpoints with curl or Postman

---

## 🎓 Additional Resources

### Django Documentation
- Official Docs: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Django ORM: https://docs.djangoproject.com/en/5.0/topics/db/

### PostgreSQL
- Official Docs: https://www.postgresql.org/docs/
- psycopg2: https://www.psycopg.org/

### Python
- Python 3 Docs: https://docs.python.org/3/

---

## ✅ Feature Checklist

### Implemented Features
- [x] Student registration with validation
- [x] Role-based authentication (admin/teacher/student)
- [x] Session management
- [x] Password hashing
- [x] Admin: View students/teachers
- [x] Admin: Add teachers
- [x] Admin: Auto-allot rooms (max 15/room)
- [x] Student: View allotment
- [x] Teacher: View room & students
- [x] All validations & edge cases
- [x] Error handling
- [x] CORS configuration
- [x] Admin panel
- [x] Management commands
- [x] Comprehensive documentation

### Not Implemented (Not Required)
- [ ] Email verification
- [ ] Password reset via email
- [ ] File uploads
- [ ] Real-time notifications
- [ ] Multi-language support

---

## 🤝 Support

### Getting Help

1. **Check Documentation**
   - Start with matching use case above
   - Check troubleshooting sections

2. **Check Logs**
   - Django console output
   - Browser console (frontend)
   - Database logs

3. **Test Independently**
   - Test backend with curl
   - Test frontend with browser DevTools
   - Verify database connection

4. **Review Settings**
   - Check `.env` file
   - Check `settings.py`
   - Check CORS configuration

---

## 📊 Quick Reference

### Commands
```bash
# Setup
python -m venv venv
pip install -r requirements.txt
python manage.py migrate
python manage.py create_admin

# Run
python manage.py runserver 0.0.0.0:8000

# Database
python manage.py makemigrations
python manage.py migrate
python manage.py shell

# Django Admin
python manage.py createsuperuser
```

### URLs
- API Base: `http://localhost:8000/api`
- Admin Panel: `http://localhost:8000/admin/`
- Health Check: `http://localhost:8000/api/auth/me`

### Credentials
- Username: `admin`
- Password: `adminpassword`

---

## 📝 Version

**Django Backend v1.0.0**

- Complete Node.js to Django conversion
- 100% functional parity
- Production-ready
- Fully documented

---

## 🎉 You're Ready!

Pick your starting point from the table at the top and dive in!

**Most users should start with**: **[QUICKSTART.md](QUICKSTART.md)**

---

**Happy Coding! 🚀**
