# Quick Start Guide - Django Backend

Get the Django backend up and running in 5 minutes!

## Prerequisites

- Python 3.10+ installed
- PostgreSQL installed and running
- Git (optional)

## Step 1: Install Dependencies

### Windows:
```bash
cd django_backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Linux/Mac:
```bash
cd django_backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 2: Configure Database

1. Create PostgreSQL database:
```sql
CREATE DATABASE exam_allotment;
```

2. Copy environment file:
```bash
cp .env.example .env
```

3. Edit `.env` with your database credentials:
```env
DB_NAME=exam_allotment
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

## Step 3: Initialize Database

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py create_admin
```

## Step 4: Run Server

```bash
python manage.py runserver 0.0.0.0:8000
```

## Step 5: Test API

```bash
curl http://localhost:8000/api/auth/me
```

Expected response: `null` (no user logged in)

## Step 6: Login as Admin

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"adminpassword","role":"admin"}' \
  -c cookies.txt
```

## Done! 🎉

Your Django backend is now running at `http://localhost:8000`

### Next Steps:

1. **Admin Panel**: Visit `http://localhost:8000/admin/` (username: `admin`, password: `adminpassword`)

2. **API Documentation**: See `API_DOCUMENTATION.md` for all endpoints

3. **Frontend Integration**: Update frontend API URL to `http://localhost:8000/api`

4. **Add Data**:
   - Register students via POST `/api/auth/register-student`
   - Add teachers via POST `/api/admin/teachers` (as admin)
   - Allot rooms via POST `/api/admin/allot` (as admin)

### Default Credentials:
- **Username**: `admin`
- **Password**: `adminpassword`

**Important**: Change the admin password in production!

## Troubleshooting

### "Can't connect to database"
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists: `psql -U postgres -l`

### "Port already in use"
```bash
python manage.py runserver 0.0.0.0:8001
```

### "Module not found"
```bash
pip install -r requirements.txt
```

### Reset Database
```bash
python manage.py flush
python manage.py create_admin
```

## Quick Test Script

Save as `test.sh`:

```bash
#!/bin/bash
BASE_URL="http://localhost:8000/api"

echo "Testing API..."

# Test 1: Get current user (should be null)
echo "1. GET /auth/me"
curl -s $BASE_URL/auth/me
echo ""

# Test 2: Login as admin
echo "2. POST /auth/login (admin)"
curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"adminpassword","role":"admin"}' \
  -c cookies.txt
echo ""

# Test 3: Get current user (should be admin)
echo "3. GET /auth/me (authenticated)"
curl -s $BASE_URL/auth/me -b cookies.txt
echo ""

# Test 4: Get students
echo "4. GET /admin/students"
curl -s $BASE_URL/admin/students -b cookies.txt
echo ""

echo "Tests complete!"
```

Run with: `chmod +x test.sh && ./test.sh`

---

**For more details, see `README.md` and `API_DOCUMENTATION.md`**
