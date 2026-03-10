# API Documentation - Exam Allotment System

Complete API reference for the Django backend.

## Base URL

```
Development: http://localhost:8000/api
Production: https://your-domain.com/api
```

## Authentication

All authenticated endpoints require a valid session cookie. The API uses session-based authentication (cookies).

**Important**: Include credentials in requests:
- Fetch API: `credentials: 'include'`
- Axios: `withCredentials: true`
- curl: `-b cookies.txt` and `-c cookies.txt`

---

## Authentication Endpoints

### Register Student

Register a new student account.

**Endpoint**: `POST /api/auth/register-student`

**Request Body**:
```json
{
  "username": "S001",
  "name": "John Doe",
  "password": "password123",
  "confirmPassword": "password123"
}
```

**Success Response** (201 Created):
```json
{
  "id": 1,
  "username": "S001",
  "name": "John Doe",
  "role": "student"
}
```

**Error Responses**:
- 400 Bad Request:
  ```json
  {
    "message": "Roll Number already registered",
    "field": "username"
  }
  ```
- 400 Bad Request:
  ```json
  {
    "message": "Passwords don't match",
    "field": "confirmPassword"
  }
  ```

---

### Login

Login for admin, teacher, or student.

**Endpoint**: `POST /api/auth/login`

**Request Body**:
```json
{
  "username": "admin",
  "password": "adminpassword",
  "role": "admin"
}
```

**Success Response** (200 OK):
```json
{
  "id": 1,
  "username": "admin",
  "name": "System Administrator",
  "role": "admin"
}
```

**Error Responses**:
- 401 Unauthorized:
  ```json
  {
    "message": "Invalid credentials or incorrect role"
  }
  ```

---

### Logout

Logout the current user.

**Endpoint**: `POST /api/auth/logout`

**Success Response** (200 OK):
```
(Empty response)
```

---

### Get Current User

Get information about the currently logged-in user.

**Endpoint**: `GET /api/auth/me`

**Success Response** (200 OK):
```json
{
  "id": 1,
  "username": "admin",
  "name": "System Administrator",
  "role": "admin"
}
```

**Response when not logged in** (200 OK):
```json
null
```

---

## Admin Endpoints

All admin endpoints require authentication and admin role.

**Authorization**: Session with role = "admin"

**Error Responses (All Endpoints)**:
- 401 Unauthorized:
  ```json
  {
    "message": "Unauthorized"
  }
  ```
- 403 Forbidden:
  ```json
  {
    "message": "Forbidden"
  }
  ```

---

### Get All Students

Get a list of all registered students.

**Endpoint**: `GET /api/admin/students`

**Success Response** (200 OK):
```json
[
  {
    "id": 2,
    "username": "S001",
    "name": "John Doe",
    "role": "student"
  },
  {
    "id": 3,
    "username": "S002",
    "name": "Jane Smith",
    "role": "student"
  }
]
```

---

### Get All Teachers

Get a list of all registered teachers.

**Endpoint**: `GET /api/admin/teachers`

**Success Response** (200 OK):
```json
[
  {
    "id": 4,
    "username": "T001",
    "name": "Dr. Brown",
    "role": "teacher"
  },
  {
    "id": 5,
    "username": "T002",
    "name": "Prof. Wilson",
    "role": "teacher"
  }
]
```

---

### Add Teacher

Add a new teacher account.

**Endpoint**: `POST /api/admin/teachers`

**Request Body**:
```json
{
  "username": "T001",
  "name": "Dr. Brown",
  "password": "teacher123"
}
```

**Success Response** (201 Created):
```json
{
  "id": 4,
  "username": "T001",
  "name": "Dr. Brown",
  "role": "teacher"
}
```

**Error Responses**:
- 400 Bad Request:
  ```json
  {
    "message": "Username already exists",
    "field": "username"
  }
  ```

---

### Auto-Allot Students

Automatically allocate students to rooms with teachers.

**Logic**:
- Maximum 15 students per room
- Students are randomly shuffled
- One teacher per room
- Clears previous allotments before creating new ones

**Endpoint**: `POST /api/admin/allot`

**Request Body**: (Empty)

**Success Response** (200 OK):
```json
{
  "message": "Allocation successful",
  "roomsCreated": 3,
  "studentsAllotted": 45
}
```

**Error Responses**:
- 400 Bad Request:
  ```json
  {
    "message": "No students registered yet."
  }
  ```
- 400 Bad Request:
  ```json
  {
    "message": "Not enough teachers. Need 3 teachers for 45 students (max 15 per room), but only have 2."
  }
  ```

---

## Student Endpoints

All student endpoints require authentication and student role.

**Authorization**: Session with role = "student"

---

### Get Student Allotment

Get the room allotment for the logged-in student.

**Endpoint**: `GET /api/student/allotment`

**Success Response** (200 OK):
```json
{
  "room": {
    "id": 1,
    "name": "Room 1",
    "teacher_id": 4
  },
  "allotment": {
    "id": 1,
    "student_id": 2,
    "room_id": 1,
    "seat_number": 5
  }
}
```

**Response when not allotted** (200 OK):
```json
null
```

---

## Teacher Endpoints

All teacher endpoints require authentication and teacher role.

**Authorization**: Session with role = "teacher"

---

### Get Teacher Room

Get the room assigned to the logged-in teacher and all students in that room.

**Endpoint**: `GET /api/teacher/room`

**Success Response** (200 OK):
```json
{
  "room": {
    "id": 1,
    "name": "Room 1",
    "teacher_id": 4
  },
  "students": [
    {
      "student": {
        "id": 2,
        "username": "S001",
        "name": "John Doe",
        "role": "student"
      },
      "seatNumber": 1
    },
    {
      "student": {
        "id": 3,
        "username": "S002",
        "name": "Jane Smith",
        "role": "student"
      },
      "seatNumber": 2
    }
  ]
}
```

**Response when no room assigned** (200 OK):
```json
null
```

---

## Error Handling

All endpoints follow consistent error response formats:

### 400 Bad Request
Validation errors or business logic errors.

```json
{
  "message": "Error description",
  "field": "fieldName"  // Optional, for field-specific errors
}
```

### 401 Unauthorized
User is not authenticated.

```json
{
  "message": "Unauthorized"
}
```

### 403 Forbidden
User doesn't have permission (wrong role).

```json
{
  "message": "Forbidden"
}
```

### 500 Internal Server Error
Server-side error.

```json
{
  "message": "Internal server error"
}
```

---

## Usage Examples

### JavaScript (Fetch)

```javascript
// Register student
const response = await fetch('http://localhost:8000/api/auth/register-student', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  credentials: 'include',  // Important for session cookies
  body: JSON.stringify({
    username: 'S001',
    name: 'John Doe',
    password: 'password123',
    confirmPassword: 'password123'
  })
});

const data = await response.json();
console.log(data);
```

```javascript
// Login
const response = await fetch('http://localhost:8000/api/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  credentials: 'include',
  body: JSON.stringify({
    username: 'admin',
    password: 'adminpassword',
    role: 'admin'
  })
});

const user = await response.json();
```

```javascript
// Get current user
const response = await fetch('http://localhost:8000/api/auth/me', {
  credentials: 'include'
});

const user = await response.json();
```

### Python (requests)

```python
import requests

# Create session to maintain cookies
session = requests.Session()

# Register student
response = session.post('http://localhost:8000/api/auth/register-student', json={
    'username': 'S001',
    'name': 'John Doe',
    'password': 'password123',
    'confirmPassword': 'password123'
})
print(response.json())

# Login
response = session.post('http://localhost:8000/api/auth/login', json={
    'username': 'admin',
    'password': 'adminpassword',
    'role': 'admin'
})
user = response.json()

# Get students (authenticated)
response = session.get('http://localhost:8000/api/admin/students')
students = response.json()
```

### curl

```bash
# Save cookies to file
COOKIES="cookies.txt"

# Register student
curl -X POST http://localhost:8000/api/auth/register-student \
  -H "Content-Type: application/json" \
  -d '{"username":"S001","name":"John Doe","password":"password123","confirmPassword":"password123"}' \
  -c $COOKIES

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"adminpassword","role":"admin"}' \
  -c $COOKIES

# Get current user (with cookies)
curl -X GET http://localhost:8000/api/auth/me \
  -b $COOKIES

# Get students (authenticated)
curl -X GET http://localhost:8000/api/admin/students \
  -b $COOKIES
```

---

## Rate Limiting

Currently no rate limiting is implemented. Consider adding rate limiting in production.

---

## CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:5000`
- Other origins configured in `.env`

Credentials (cookies) are allowed for all configured origins.

---

## Session Management

- **Session Duration**: 24 hours (86400 seconds)
- **Session Storage**: Database-backed (production) or memory (development)
- **Cookie Name**: `sessionid`
- **Cookie Attributes**: HttpOnly, SameSite=Lax

Sessions are automatically created on login and destroyed on logout.

---

## Testing Workflow

1. **Register a student**:
   ```
   POST /api/auth/register-student
   ```

2. **Login as admin**:
   ```
   POST /api/auth/login (role: admin)
   ```

3. **Add teachers**:
   ```
   POST /api/admin/teachers
   ```

4. **Allot students to rooms**:
   ```
   POST /api/admin/allot
   ```

5. **Login as student** and check allotment:
   ```
   POST /api/auth/login (role: student)
   GET /api/student/allotment
   ```

6. **Login as teacher** and view room:
   ```
   POST /api/auth/login (role: teacher)
   GET /api/teacher/room
   ```

---

## Default Accounts

After initial setup:

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `adminpassword` |

**Change the admin password in production!**
