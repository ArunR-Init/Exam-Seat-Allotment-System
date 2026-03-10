"""
Template-rendering views for the Exam Allotment System.
These views render HTML templates for the web interface.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db import transaction
from datetime import datetime
import random
import math

from .models import User, Room, Allotment


# ==================== Public Views ====================

def home_view(request):
    """Home page."""
    return render(request, 'home.html')


@require_http_methods(["GET", "POST"])
def register_view(request):
    """Student registration page."""
    # If student is already logged in, redirect to their dashboard
    if request.user.is_authenticated and request.user.role == 'student':
        return redirect('student_dashboard')
    
    # If non-student is logged in, logout first
    if request.user.is_authenticated and request.user.role != 'student':
        auth_logout(request)
        messages.info(request, 'Student registration only. Please register or login as a student.')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        name = request.POST.get('name', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirmPassword', '')
        
        # Validation
        if not username or not name or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'register.html')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
            return render(request, 'register.html')
        
        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Roll Number already registered.')
            return render(request, 'register.html')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            name=name,
            password=password,
            role='student'
        )
        
        # Log the user in
        auth_login(request, user)
        
        messages.success(request, 'Registration successful! Welcome.')
        return redirect('student_dashboard')
    
    return render(request, 'register.html')


@require_http_methods(["GET", "POST"])
def login_view(request, role):
    """Login page for different roles (admin, teacher, student)."""
    # Validate role
    if role not in ['admin', 'teacher', 'student']:
        return redirect('home')
    
    # If user is authenticated with the SAME role, redirect to dashboard
    if request.user.is_authenticated and request.user.role == role:
        return redirect('dashboard')
    
    # If user is authenticated with DIFFERENT role, logout first
    if request.user.is_authenticated and request.user.role != role:
        auth_logout(request)
        messages.info(request, 'Please login with the correct credentials.')
    
    # Role configuration
    role_configs = {
        'admin': {
            'title': 'Admin Portal',
            'icon': 'shield-check',
            'icon_color': 'text-slate-700',
            'color': 'border-t-slate-800',
            'bg': 'bg-slate-100'
        },
        'teacher': {
            'title': 'Faculty Portal',
            'icon': 'graduation-cap',
            'icon_color': 'text-indigo-500',
            'color': 'border-t-indigo-400',
            'bg': 'bg-indigo-50'
        },
        'student': {
            'title': 'Student Portal',
            'icon': 'users',
            'icon_color': 'text-blue-500',
            'color': 'border-t-blue-400',
            'bg': 'bg-blue-50'
        }
    }
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'login.html', {
                'role': role,
                'role_config': role_configs[role]
            })
        
        try:
            user = User.objects.get(username=username)
            
            # Check password and role
            if not user.check_password(password) or user.role != role:
                messages.error(request, 'Invalid credentials or incorrect role.')
                return render(request, 'login.html', {
                    'role': role,
                    'role_config': role_configs[role]
                })
            
            # Authenticate and login
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth_login(request, user)
            
            messages.success(request, f'Welcome back, {user.name}!')
            return redirect('dashboard')
        
        except User.DoesNotExist:
            messages.error(request, 'Invalid credentials or incorrect role.')
            return render(request, 'login.html', {
                'role': role,
                'role_config': role_configs[role]
            })
    
    return render(request, 'login.html', {
        'role': role,
        'role_config': role_configs[role]
    })


@login_required
def logout_view(request):
    """Logout view."""
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def dashboard_view(request):
    """Redirect to appropriate dashboard based on role."""
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    elif request.user.role == 'teacher':
        return redirect('teacher_dashboard')
    elif request.user.role == 'student':
        return redirect('student_dashboard')
    else:
        return redirect('home')


# ==================== Student Views ====================

@login_required
def student_dashboard_view(request):
    """Student dashboard page."""
    if request.user.role != 'student':
        messages.error(request, 'Access denied. Students only.')
        return redirect('dashboard')
    
    show_details = request.GET.get('reveal') == 'true'
    allotment = None
    
    if show_details:
        try:
            allotment = Allotment.objects.select_related('room', 'room__teacher').get(student=request.user)
        except Allotment.DoesNotExist:
            pass
    
    return render(request, 'student_dashboard.html', {
        'show_details': show_details,
        'allotment': allotment,
        'today': datetime.now().strftime('%B %d, %Y')
    })


# ==================== Teacher Views ====================

@login_required
def teacher_dashboard_view(request):
    """Teacher dashboard page."""
    if request.user.role != 'teacher':
        messages.error(request, 'Access denied. Teachers only.')
        return redirect('dashboard')
    
    show_details = request.GET.get('reveal') == 'true'
    room = None
    students = []
    
    if show_details:
        try:
            room = Room.objects.get(teacher=request.user)
            students = Allotment.objects.filter(room=room).select_related('student').order_by('seat_number')
        except Room.DoesNotExist:
            pass
    
    return render(request, 'teacher_dashboard.html', {
        'show_details': show_details,
        'room': room,
        'students': students
    })


# ==================== Admin Views ====================

@login_required
def admin_dashboard_view(request):
    """Admin dashboard page."""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admins only.')
        return redirect('dashboard')
    
    # Get all data
    students = list(User.objects.filter(role='student').order_by('id'))
    teachers = User.objects.filter(role='teacher').order_by('id')
    rooms = Room.objects.all()
    
    # Add allotment info to students (use a custom attribute)
    for student in students:
        try:
            student.allotment_info = Allotment.objects.get(student=student)
        except Allotment.DoesNotExist:
            student.allotment_info = None
    
    context = {
        'students': students,
        'teachers': teachers,
        'students_count': len(students),
        'teachers_count': teachers.count(),
        'rooms_count': rooms.count()
    }
    
    return render(request, 'admin_dashboard.html', context)


@login_required
@require_http_methods(["POST"])
def add_teacher_view(request):
    """Add a new teacher (admin only)."""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admins only.')
        return redirect('dashboard')
    
    name = request.POST.get('name', '').strip()
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')
    
    # Validation
    if not name or not username or not password:
        messages.error(request, 'All fields are required.')
        from django.http import HttpResponseRedirect
        from django.urls import reverse
        return HttpResponseRedirect(reverse('admin_dashboard') + '#teachers')
    
    if len(password) < 6:
        messages.error(request, 'Password must be at least 6 characters.')
        from django.http import HttpResponseRedirect
        from django.urls import reverse
        return HttpResponseRedirect(reverse('admin_dashboard') + '#teachers')
    
    # Check if username exists
    if User.objects.filter(username=username).exists():
        messages.error(request, 'Username already exists.')
        from django.http import HttpResponseRedirect
        from django.urls import reverse
        return HttpResponseRedirect(reverse('admin_dashboard') + '#teachers')
    
    # Create teacher
    User.objects.create_user(
        username=username,
        name=name,
        password=password,
        role='teacher'
    )
    
    messages.success(request, f'Teacher {name} added successfully!')
    from django.http import HttpResponseRedirect
    from django.urls import reverse
    return HttpResponseRedirect(reverse('admin_dashboard') + '#teachers')


@login_required
@require_http_methods(["POST"])
def allot_rooms_view(request):
    """Allocate students to rooms (admin only)."""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admins only.')
        return redirect('dashboard')
    
    # Get all students and teachers
    students = list(User.objects.filter(role='student'))
    teachers = list(User.objects.filter(role='teacher'))
    
    if len(students) == 0:
        messages.error(request, 'No students registered yet.')
        return redirect('admin_dashboard')
    
    # Calculate needed rooms (15 students per room)
    needed_rooms = math.ceil(len(students) / 15)
    
    if len(teachers) < needed_rooms:
        messages.error(request, 
            f'Not enough teachers. Need {needed_rooms} teachers for {len(students)} students (max 15 per room), but only have {len(teachers)}.')
        return redirect('admin_dashboard')
    
    # Use transaction to ensure atomicity
    with transaction.atomic():
        # Clear old allotments and rooms
        Allotment.objects.all().delete()
        Room.objects.all().delete()
        
        # Shuffle students randomly
        random.shuffle(students)
        
        students_allotted = 0
        rooms_created = 0
        
        # Create rooms and assign students
        for i in range(needed_rooms):
            room_teacher = teachers[i]
            
            # Create room
            room = Room.objects.create(
                name=f"Room {i + 1}",
                teacher=room_teacher
            )
            rooms_created += 1
            
            # Get students for this room (max 15)
            students_for_room = students[i * 15:(i + 1) * 15]
            
            # Create allotments for each student
            for j, student in enumerate(students_for_room):
                Allotment.objects.create(
                    room=room,
                    student=student,
                    seat_number=j + 1
                )
                students_allotted += 1
    
    messages.success(request, 
        f'Allocation successful! Created {rooms_created} rooms and allotted {students_allotted} students.')
    return redirect('admin_dashboard')
