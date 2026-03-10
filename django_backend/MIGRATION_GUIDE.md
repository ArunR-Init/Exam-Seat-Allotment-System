# Migration Guide: Node.js to Django

This document explains how the Node.js/Express backend was converted to Django while maintaining exact functionality.

## Architecture Comparison

| Component | Node.js/Express | Django | Notes |
|-----------|----------------|---------|-------|
| Web Framework | Express 5.0 | Django 5.0 + DRF | Same functionality |
| Database | PostgreSQL | PostgreSQL | No change |
| ORM | Drizzle | Django ORM | Different syntax, same queries |
| Validation | Zod | DRF Serializers | Same validation rules |
| Sessions | express-session | Django sessions | Same behavior |
| Password Hashing | Plain text | Django's PBKDF2 | More secure in Django |

## File Mapping

### Node.js → Django Mapping

| Node.js File | Django Equivalent | Purpose |
|--------------|------------------|---------|
| `server/index.ts` | `config/wsgi.py`, `config/asgi.py` | Server entry point |
| `server/routes.ts` | `exam_app/views.py` + `exam_app/urls.py` | Route definitions & handlers |
| `shared/schema.ts` | `exam_app/models.py` + `exam_app/serializers.py` | Database schema & validation |
| `server/storage.ts` | `exam_app/models.py` (ORM methods) | Database operations |
| `server/db.ts` | `config/settings.py` (DATABASES) | Database configuration |
| `package.json` | `requirements.txt` | Dependencies |
| `.env.example` | `.env.example` | Environment variables |

## Code Conversion Examples

### 1. User Model

**Node.js (Drizzle):**
```typescript
export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  role: text("role", { enum: ["admin", "teacher", "student"] }).notNull(),
  username: text("username").notNull().unique(),
  name: text("name").notNull(),
  password: text("password").notNull(),
});
```

**Django:**
```python
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=128)
```

### 2. Validation Schema

**Node.js (Zod):**
```typescript
export const studentRegisterSchema = z.object({
  username: z.string().min(1, "Roll Number is required"),
  name: z.string().min(1, "Name is required"),
  password: z.string().min(1, "Password is required"),
  confirmPassword: z.string().min(1, "Confirm Password is required")
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});
```

**Django (DRF Serializer):**
```python
class StudentRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, error_messages={'required': 'Roll Number is required'})
    name = serializers.CharField(required=True, error_messages={'required': 'Name is required'})
    password = serializers.CharField(required=True, write_only=True, error_messages={'required': 'Password is required'})
    confirmPassword = serializers.CharField(required=True, write_only=True, error_messages={'required': 'Confirm Password is required'})
    
    def validate(self, data):
        if data.get('password') != data.get('confirmPassword'):
            raise serializers.ValidationError({
                'confirmPassword': "Passwords don't match"
            })
        return data
```

### 3. API Route Handler

**Node.js (Express):**
```typescript
app.post(api.auth.registerStudent.path, async (req, res) => {
  try {
    const input = api.auth.registerStudent.input.parse(req.body);
    
    const existingUser = await storage.getUserByUsername(input.username);
    if (existingUser) {
      return res.status(400).json({ message: "Roll Number already registered", field: "username" });
    }

    const user = await storage.createUser({
      username: input.username,
      name: input.name,
      password: input.password,
      role: "student"
    });

    req.session.userId = user.id;
    req.session.role = user.role;
    res.status(201).json(user);
  } catch (err) {
    if (err instanceof z.ZodError) {
      return res.status(400).json({ message: err.errors[0].message, field: err.errors[0].path.join('.') });
    }
    return res.status(500).json({ message: "Internal server error" });
  }
});
```

**Django (DRF):**
```python
@api_view(['POST'])
def register_student(request):
    serializer = StudentRegisterSerializer(data=request.data)
    
    if not serializer.is_valid():
        errors = serializer.errors
        first_field = list(errors.keys())[0]
        first_error = errors[first_field][0] if isinstance(errors[first_field], list) else str(errors[first_field])
        return Response(
            {'message': str(first_error), 'field': first_field},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=serializer.validated_data['username']).exists():
        return Response(
            {'message': 'Roll Number already registered', 'field': 'username'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = serializer.save()
    
    request.session['userId'] = user.id
    request.session['role'] = user.role
    
    return Response(
        UserSerializer(user).data,
        status=status.HTTP_201_CREATED
    )
```

### 4. Database Queries

**Node.js (Drizzle):**
```typescript
// Get user by username
const [user] = await db.select().from(users).where(eq(users.username, username));

// Get users by role
const students = await db.select().from(users).where(eq(users.role, 'student'));

// Create user
const [user] = await db.insert(users).values(insertUser).returning();

// Delete all
await db.delete(allotments);
```

**Django (ORM):**
```python
# Get user by username
user = User.objects.get(username=username)

# Get users by role
students = User.objects.filter(role='student')

# Create user
user = User.objects.create(**user_data)

# Delete all
Allotment.objects.all().delete()
```

### 5. Session Management

**Node.js:**
```typescript
// Session setup
app.use(session({
  cookie: { maxAge: 86400000 },
  store: new SessionStore({
    checkPeriod: 86400000
  }),
  resave: false,
  saveUninitialized: false,
  secret: process.env.SESSION_SECRET || 'keyboard cat'
}));

// Set session
req.session.userId = user.id;
req.session.role = user.role;

// Check session
if (!req.session.userId) return res.status(401).json({ message: 'Unauthorized' });
```

**Django:**
```python
# Session settings in settings.py
SESSION_COOKIE_AGE = 86400
SESSION_SAVE_EVERY_REQUEST = False
SESSION_COOKIE_HTTPONLY = True

# Set session (in view)
request.session['userId'] = user.id
request.session['role'] = user.role

# Check session
if not request.session.get('userId'):
    return Response({'message': 'Unauthorized'}, status=401)
```

## Functional Equivalence Checklist

### Authentication ✅
- [x] Student registration with password confirmation
- [x] Login with role validation
- [x] Session-based auth
- [x] Logout
- [x] Get current user

### Authorization ✅
- [x] Admin-only endpoints
- [x] Teacher-only endpoints
- [x] Student-only endpoints
- [x] 401 for unauthenticated
- [x] 403 for unauthorized role

### Admin Features ✅
- [x] View all students
- [x] View all teachers
- [x] Add teachers with validation
- [x] Auto-allotment algorithm (15 per room)
- [x] Random student shuffling
- [x] Teacher availability check
- [x] Clear old allotments

### Student Features ✅
- [x] View room allotment
- [x] View seat number
- [x] Return null if not allotted

### Teacher Features ✅
- [x] View assigned room
- [x] View students in room
- [x] Students sorted by seat number
- [x] Return null if no room assigned

### Validation ✅
- [x] Required fields
- [x] Username uniqueness
- [x] Password confirmation
- [x] Role validation
- [x] Custom error messages
- [x] Field-level errors

### Edge Cases ✅
- [x] No students registered (allotment)
- [x] Insufficient teachers (allotment)
- [x] No allotment found (student)
- [x] No room assigned (teacher)
- [x] Invalid credentials
- [x] Wrong role for login
- [x] Session expiry

## Benefits of Django Version

1. **Better Security**: Built-in password hashing (PBKDF2)
2. **Admin Interface**: Built-in admin panel at `/admin/`
3. **ORM Power**: More robust query capabilities
4. **Middleware**: Better request/response handling
5. **Testing**: Better testing framework
6. **Documentation**: Auto-generated API docs possible
7. **Ecosystem**: Vast Python package ecosystem

## Running Both Versions

You can run both backends simultaneously for comparison:

- **Node.js Backend**: `http://localhost:5000`
- **Django Backend**: `http://localhost:8000`

Update the frontend API base URL to switch between them.

## Testing Equivalence

```bash
# Test Node.js version
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"adminpassword","role":"admin"}'

# Test Django version (should return same response)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"adminpassword","role":"admin"}'
```

Both should return identical JSON responses.

## Migration Checklist

If migrating data from Node.js to Django:

1. ✅ Export data from PostgreSQL
2. ✅ Note: Passwords need re-hashing for Django
3. ✅ Import users (they'll need to reset passwords OR use management command)
4. ✅ Import rooms and allotments as-is
5. ✅ Run Django migrations
6. ✅ Test all endpoints
7. ✅ Update frontend API URL

## Conclusion

The Django implementation is a 1:1 functional replica of the Node.js version. All business logic, validations, error handling, and edge cases have been preserved. The only differences are:

1. **Better password security** (Django's hashing vs plain text)
2. **Additional admin interface** (Django admin panel)
3. **Python instead of TypeScript** (language difference)

The API contract remains identical, so the frontend requires no changes.
