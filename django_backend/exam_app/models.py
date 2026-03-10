"""
Django models for the Exam Allotment System.
Replicating the schema from Node.js/Drizzle implementation.
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """Custom user manager for handling user creation."""
    
    def create_user(self, username, password=None, **extra_fields):
        """Create and save a regular user."""
        if not username:
            raise ValueError('The Username field must be set')
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        """Create and save a superuser."""
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('name', 'Admin')
        
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model matching the Node.js schema.
    Fields: id (auto), role, username, name, password
    """
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    username = models.CharField(max_length=255, unique=True)  # Admin/Teacher username or Student Roll Number
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=128)  # Django handles hashing
    
    # Required by Django for admin
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'role']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} ({self.role})"
    
    def save(self, *args, **kwargs):
        """Override save to handle password hashing for plain text passwords."""
        # Only hash if password doesn't look like it's already hashed
        if self.password and not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)
        super().save(*args, **kwargs)


class Room(models.Model):
    """
    Room model for exam rooms.
    Fields: id (auto), name, teacher_id (reference to User)
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_room',
        db_column='teacher_id'
    )
    
    class Meta:
        db_table = 'rooms'
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
    
    def __str__(self):
        return f"{self.name} - {self.teacher.name}"


class Allotment(models.Model):
    """
    Allotment model for student room assignments.
    Fields: id (auto), student_id, room_id, seat_number
    """
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='allotment',
        db_column='student_id'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='allotments',
        db_column='room_id'
    )
    seat_number = models.IntegerField()
    
    class Meta:
        db_table = 'allotments'
        verbose_name = 'Allotment'
        verbose_name_plural = 'Allotments'
        unique_together = ['student', 'room']
    
    def __str__(self):
        return f"{self.student.username} - {self.room.name} - Seat {self.seat_number}"
