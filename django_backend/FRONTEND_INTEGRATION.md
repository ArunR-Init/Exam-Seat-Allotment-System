# Frontend Integration Guide

How to connect the existing React frontend with the new Django backend.

---

## Overview

The Django backend maintains **100% API compatibility** with the original Node.js backend. This means:

✅ No changes to frontend code required  
✅ Same endpoints  
✅ Same request/response formats  
✅ Same authentication mechanism  
✅ Same error handling  

---

## Quick Integration

### Option 1: Update API Base URL (Recommended)

If your frontend has a centralized API configuration:

**Before (Node.js):**
```javascript
// src/lib/api.ts or similar
const API_BASE_URL = 'http://localhost:5000/api';
```

**After (Django):**
```javascript
// src/lib/api.ts or similar
const API_BASE_URL = 'http://localhost:8000/api';
```

### Option 2: Environment Variable

**Create `.env` in frontend:**
```env
VITE_API_URL=http://localhost:8000/api
```

**Use in code:**
```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
```

---

## Complete Frontend Setup

### Step 1: Start Django Backend

```bash
cd django_backend
python manage.py runserver 0.0.0.0:8000
```

Backend will be available at: `http://localhost:8000`

### Step 2: Update Frontend Configuration

#### Check Your Fetch/Axios Configuration

**Fetch API (ensure credentials are included):**
```javascript
fetch('http://localhost:8000/api/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  credentials: 'include',  // IMPORTANT: Include cookies
  body: JSON.stringify(data)
});
```

**Axios (ensure credentials are enabled):**
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  withCredentials: true,  // IMPORTANT: Include cookies
  headers: {
    'Content-Type': 'application/json'
  }
});
```

### Step 3: Start Frontend

```bash
cd client
npm install  # if not already done
npm run dev
```

Frontend will be available at: `http://localhost:5173`

---

## Testing Integration

### Test 1: Landing Page
1. Visit `http://localhost:5173`
2. Should load without errors
3. Check browser console for any API errors

### Test 2: Student Registration
1. Navigate to student registration
2. Fill in the form:
   - Roll Number: `S001`
   - Name: `John Doe`
   - Password: `password123`
   - Confirm Password: `password123`
3. Submit
4. Should redirect to student dashboard

### Test 3: Admin Login
1. Navigate to admin login
2. Credentials:
   - Username: `admin`
   - Password: `adminpassword`
3. Should redirect to admin dashboard

### Test 4: Add Teacher (Admin)
1. Login as admin
2. Navigate to "Add Teacher" section
3. Fill in teacher details
4. Submit
5. Teacher should appear in list

### Test 5: Allot Rooms (Admin)
1. Ensure at least 1 student and 1 teacher exist
2. Click "Allot Rooms" button
3. Should see success message

### Test 6: Student View Allotment
1. Login as a student (who has been allotted)
2. Navigate to student dashboard
3. Should see room name and seat number

### Test 7: Teacher View Room
1. Login as a teacher (who has been assigned)
2. Navigate to teacher dashboard
3. Should see room and list of students

---

## Common Integration Issues & Solutions

### Issue 1: CORS Errors

**Error:**
```
Access to fetch at 'http://localhost:8000/api/...' from origin 'http://localhost:5173' 
has been blocked by CORS policy
```

**Solution:**
Edit Django `django_backend/.env`:
```env
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5000,http://127.0.0.1:5173
```

Restart Django server.

---

### Issue 2: Cookies Not Being Sent

**Error:**
Authentication works but subsequent requests fail with 401 Unauthorized.

**Solution:**
Ensure `credentials: 'include'` (Fetch) or `withCredentials: true` (Axios) is set:

```javascript
// Fetch
fetch(url, {
  credentials: 'include',  // Add this
  // ... other options
});

// Axios
axios.create({
  withCredentials: true,  // Add this
  // ... other options
});
```

---

### Issue 3: Session Not Persisting

**Error:**
User is logged out after page refresh.

**Solution:**
1. Check that cookies are being stored (Browser DevTools → Application → Cookies)
2. Ensure `credentials: 'include'` is set on ALL requests
3. Check Django session settings in `settings.py`:
   ```python
   SESSION_COOKIE_AGE = 86400  # 24 hours
   SESSION_COOKIE_HTTPONLY = True
   SESSION_COOKIE_SAMESITE = 'Lax'
   ```

---

### Issue 4: CSRF Token Errors

**Error:**
```
CSRF verification failed. Request aborted.
```

**Solution:**
Django sessions handle CSRF automatically. Ensure:
1. You're using `credentials: 'include'`
2. You're not sending manual CSRF tokens (not needed with sessions)

If needed, add to Django settings:
```python
CSRF_COOKIE_HTTPONLY = False
```

---

### Issue 5: Different Response Format

**Error:**
Frontend expects different field names.

**Solution:**
The Django backend matches the exact response format. Check:
1. `UserSerializer` in `serializers.py` outputs: `id`, `username`, `name`, `role`
2. This matches Node.js User model exactly

If you find discrepancies, check the serializer field names.

---

## Side-by-Side Testing

You can run both backends simultaneously to compare:

### Terminal 1: Node.js Backend
```bash
cd Attached-Assets
npm run dev
```
Runs at: `http://localhost:5000`

### Terminal 2: Django Backend
```bash
cd django_backend
python manage.py runserver 0.0.0.0:8000
```
Runs at: `http://localhost:8000`

### Terminal 3: Frontend
```bash
cd client
npm run dev
```
Runs at: `http://localhost:5173`

Switch between backends by changing the API URL in your frontend.

---

## API Endpoint Verification

Test each endpoint with curl to verify compatibility:

### Test Authentication
```bash
# Register Student
curl -X POST http://localhost:8000/api/auth/register-student \
  -H "Content-Type: application/json" \
  -d '{"username":"S001","name":"John Doe","password":"pass123","confirmPassword":"pass123"}' \
  -c cookies.txt

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"adminpassword","role":"admin"}' \
  -c cookies.txt

# Get Current User
curl http://localhost:8000/api/auth/me -b cookies.txt

# Logout
curl -X POST http://localhost:8000/api/auth/logout -b cookies.txt
```

### Test Admin Endpoints
```bash
# Get Students
curl http://localhost:8000/api/admin/students -b cookies.txt

# Get Teachers
curl http://localhost:8000/api/admin/teachers -b cookies.txt

# Add Teacher
curl -X POST http://localhost:8000/api/admin/teachers \
  -H "Content-Type: application/json" \
  -d '{"username":"T001","name":"Dr. Smith","password":"teacher123"}' \
  -b cookies.txt

# Allot Rooms
curl -X POST http://localhost:8000/api/admin/allot -b cookies.txt
```

### Test Student Endpoint
```bash
# Get Allotment (login as student first)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"S001","password":"pass123","role":"student"}' \
  -c cookies.txt

curl http://localhost:8000/api/student/allotment -b cookies.txt
```

### Test Teacher Endpoint
```bash
# Get Room (login as teacher first)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"T001","password":"teacher123","role":"teacher"}' \
  -c cookies.txt

curl http://localhost:8000/api/teacher/room -b cookies.txt
```

---

## Frontend Code Examples

### Complete API Client Setup

```javascript
// src/lib/api.ts
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor (optional)
api.interceptors.request.use(
  config => {
    console.log(`${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  error => Promise.reject(error)
);

// Response interceptor (optional)
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      console.log('Unauthorized - redirecting to login');
      // window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

### Usage in Components

```javascript
// src/hooks/useAuth.ts
import { useMutation, useQuery } from '@tanstack/react-query';
import api from '../lib/api';

// Register Student
export const useRegisterStudent = () => {
  return useMutation({
    mutationFn: async (data) => {
      const response = await api.post('/auth/register-student', data);
      return response.data;
    }
  });
};

// Login
export const useLogin = () => {
  return useMutation({
    mutationFn: async (data) => {
      const response = await api.post('/auth/login', data);
      return response.data;
    }
  });
};

// Get Current User
export const useCurrentUser = () => {
  return useQuery({
    queryKey: ['currentUser'],
    queryFn: async () => {
      const response = await api.get('/auth/me');
      return response.data;
    }
  });
};

// Logout
export const useLogout = () => {
  return useMutation({
    mutationFn: async () => {
      await api.post('/auth/logout');
    }
  });
};
```

---

## Browser DevTools Debugging

### Check Network Requests

1. Open DevTools (F12)
2. Go to Network tab
3. Filter by "Fetch/XHR"
4. Watch requests to `/api/*`
5. Check:
   - Status codes (200, 201, 401, etc.)
   - Request headers (Content-Type)
   - Response data
   - Cookies being sent/received

### Check Cookies

1. Open DevTools (F12)
2. Go to Application tab
3. Navigate to Cookies → `http://localhost:5173`
4. Look for `sessionid` cookie
5. Verify:
   - Cookie exists after login
   - Cookie is sent with requests
   - Cookie expires in 24 hours

### Check Console

Monitor console for:
- CORS errors
- Network errors
- API response errors
- Authentication errors

---

## Production Deployment

### Frontend Configuration

**For Production with different domain:**

```javascript
// Update API URL for production
const API_BASE_URL = 
  process.env.NODE_ENV === 'production'
    ? 'https://api.yourdomain.com/api'
    : 'http://localhost:8000/api';
```

### Django Configuration

Update `django_backend/.env` for production:

```env
DEBUG=False
ALLOWED_HOSTS=api.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
SESSION_COOKIE_SECURE=True  # Requires HTTPS
```

---

## Checklist for Integration

### Pre-Integration
- [ ] Django backend is running
- [ ] Database is set up and migrated
- [ ] Admin user is created
- [ ] CORS is configured for frontend URL

### Integration
- [ ] Frontend API URL updated
- [ ] `credentials: 'include'` is set on all requests
- [ ] Frontend can reach backend (test with curl)
- [ ] Cookies are being stored in browser

### Testing
- [ ] Student registration works
- [ ] Login works (admin, teacher, student)
- [ ] Logout works
- [ ] Admin can view students/teachers
- [ ] Admin can add teachers
- [ ] Admin can allot rooms
- [ ] Student can view allotment
- [ ] Teacher can view room

### Production
- [ ] Environment variables set
- [ ] HTTPS enabled
- [ ] CORS configured for production domains
- [ ] Session security enabled
- [ ] DEBUG=False in Django

---

## Need Help?

### Documentation
- See `API_DOCUMENTATION.md` for all endpoints
- See `README.md` for setup instructions
- See `MIGRATION_GUIDE.md` for Node.js comparison

### Debugging Steps
1. Check Django server is running: `curl http://localhost:8000/api/auth/me`
2. Check CORS settings in `.env`
3. Check browser console for errors
4. Check Network tab for failed requests
5. Check cookies are being stored
6. Verify `credentials: 'include'` is set

### Common Fixes
- Restart Django server after config changes
- Clear browser cookies if issues persist
- Check PostgreSQL is running
- Verify `.env` file exists and is correct

---

**The frontend should work seamlessly with the Django backend!**

No code changes required - just update the API URL and ensure credentials are included in requests.
