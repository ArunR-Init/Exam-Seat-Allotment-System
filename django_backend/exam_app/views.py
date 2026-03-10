"""
Views for the Exam Allotment System.
Replicating the exact functionality from Node.js/Express routes.
"""
import random
import logging
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Room, Allotment
from .serializers import (
    UserSerializer, StudentRegisterSerializer, LoginSerializer,
    TeacherCreateSerializer, RoomSerializer, AllotmentSerializer,
    StudentAllotmentResponseSerializer, TeacherRoomResponseSerializer,
    AllotmentResultSerializer
)

logger = logging.getLogger(__name__)


# ==================== Helper Functions ====================

def require_auth(request):
    """Check if user is authenticated."""
    if not request.session.get('userId'):
        return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    return None


def require_role(request, required_role):
    """Check if user has the required role."""
    if request.session.get('role') != required_role:
        return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
    return None


# ==================== Authentication Routes ====================

@api_view(['POST'])
def register_student(request):
    """
    POST /api/auth/register-student
    Register a new student.
    """
    serializer = StudentRegisterSerializer(data=request.data)
    
    if not serializer.is_valid():
        # Format errors to match Node.js response
        errors = serializer.errors
        first_field = list(errors.keys())[0]
        first_error = errors[first_field][0] if isinstance(errors[first_field], list) else str(errors[first_field])
        return Response(
            {'message': str(first_error), 'field': first_field},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if username already exists
    if User.objects.filter(username=serializer.validated_data['username']).exists():
        return Response(
            {'message': 'Roll Number already registered', 'field': 'username'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create user
    user = serializer.save()
    
    # Set session
    request.session['userId'] = user.id
    request.session['role'] = user.role
    
    return Response(
        UserSerializer(user).data,
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
def login_user(request):
    """
    POST /api/auth/login
    Login a user (admin, teacher, or student).
    """
    serializer = LoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        errors = serializer.errors
        first_field = list(errors.keys())[0]
        first_error = errors[first_field][0] if isinstance(errors[first_field], list) else str(errors[first_field])
        return Response(
            {'message': str(first_error)},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    role = serializer.validated_data['role']
    
    try:
        user = User.objects.get(username=username)
        
        # Check password and role
        if not user.check_password(password) or user.role != role:
            return Response(
                {'message': 'Invalid credentials or incorrect role'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Set session
        request.session['userId'] = user.id
        request.session['role'] = user.role
        
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_200_OK
        )
    
    except User.DoesNotExist:
        return Response(
            {'message': 'Invalid credentials or incorrect role'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
def logout_user(request):
    """
    POST /api/auth/logout
    Logout the current user.
    """
    request.session.flush()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def get_me(request):
    """
    GET /api/auth/me
    Get current user info.
    """
    user_id = request.session.get('userId')
    
    if not user_id:
        return Response(None, status=status.HTTP_200_OK)
    
    try:
        user = User.objects.get(id=user_id)
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_200_OK
        )
    except User.DoesNotExist:
        return Response(None, status=status.HTTP_200_OK)


# ==================== Admin Routes ====================

@api_view(['GET'])
def get_students(request):
    """
    GET /api/admin/students
    Get all students (admin only).
    """
    # Check authentication and authorization
    auth_check = require_auth(request)
    if auth_check:
        return auth_check
    
    role_check = require_role(request, 'admin')
    if role_check:
        return role_check
    
    students = User.objects.filter(role='student').order_by('id')
    return Response(
        UserSerializer(students, many=True).data,
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def get_teachers(request):
    """
    GET /api/admin/teachers
    Get all teachers (admin only).
    """
    # Check authentication and authorization
    auth_check = require_auth(request)
    if auth_check:
        return auth_check
    
    role_check = require_role(request, 'admin')
    if role_check:
        return role_check
    
    teachers = User.objects.filter(role='teacher').order_by('id')
    return Response(
        UserSerializer(teachers, many=True).data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def add_teacher(request):
    """
    POST /api/admin/teachers
    Add a new teacher (admin only).
    """
    # Check authentication and authorization
    auth_check = require_auth(request)
    if auth_check:
        return auth_check
    
    role_check = require_role(request, 'admin')
    if role_check:
        return role_check
    
    serializer = TeacherCreateSerializer(data=request.data)
    
    if not serializer.is_valid():
        errors = serializer.errors
        first_field = list(errors.keys())[0]
        first_error = errors[first_field][0] if isinstance(errors[first_field], list) else str(errors[first_field])
        return Response(
            {'message': str(first_error)},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if username already exists
    if User.objects.filter(username=serializer.validated_data['username']).exists():
        return Response(
            {'message': 'Username already exists', 'field': 'username'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create teacher
    teacher = serializer.save()
    
    return Response(
        UserSerializer(teacher).data,
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
def allot_rooms(request):
    """
    POST /api/admin/allot
    Allocate students to rooms (admin only).
    
    Logic:
    1. Get all students and teachers
    2. Calculate needed rooms (max 15 students per room)
    3. Check if enough teachers available
    4. Clear old allotments and rooms
    5. Shuffle students randomly
    6. Create rooms and assign students
    """
    # Check authentication and authorization
    auth_check = require_auth(request)
    if auth_check:
        return auth_check
    
    role_check = require_role(request, 'admin')
    if role_check:
        return role_check
    
    # Get all students and teachers
    students = list(User.objects.filter(role='student'))
    teachers = list(User.objects.filter(role='teacher'))
    
    if len(students) == 0:
        return Response(
            {'message': 'No students registered yet.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Calculate needed rooms (15 students per room)
    import math
    needed_rooms = math.ceil(len(students) / 15)
    
    if len(teachers) < needed_rooms:
        return Response(
            {'message': f'Not enough teachers. Need {needed_rooms} teachers for {len(students)} students (max 15 per room), but only have {len(teachers)}.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
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
    
    return Response(
        {
            'message': 'Allocation successful',
            'roomsCreated': rooms_created,
            'studentsAllotted': students_allotted
        },
        status=status.HTTP_200_OK
    )


# ==================== Student Routes ====================

@api_view(['GET'])
def get_student_allotment(request):
    """
    GET /api/student/allotment
    Get allotment details for logged-in student.
    """
    # Check authentication and authorization
    auth_check = require_auth(request)
    if auth_check:
        return auth_check
    
    role_check = require_role(request, 'student')
    if role_check:
        return role_check
    
    user_id = request.session.get('userId')
    
    try:
        allotment = Allotment.objects.select_related('room', 'room__teacher').get(student_id=user_id)
        
        return Response(
            {
                'room': RoomSerializer(allotment.room).data,
                'allotment': AllotmentSerializer(allotment).data
            },
            status=status.HTTP_200_OK
        )
    
    except Allotment.DoesNotExist:
        return Response(None, status=status.HTTP_200_OK)


# ==================== Teacher Routes ====================

@api_view(['GET'])
def get_teacher_room(request):
    """
    GET /api/teacher/room
    Get room details and students for logged-in teacher.
    """
    # Check authentication and authorization
    auth_check = require_auth(request)
    if auth_check:
        return auth_check
    
    role_check = require_role(request, 'teacher')
    if role_check:
        return role_check
    
    user_id = request.session.get('userId')
    
    try:
        room = Room.objects.get(teacher_id=user_id)
        
        # Get all allotments for this room
        allotments = Allotment.objects.filter(room=room).select_related('student').order_by('seat_number')
        
        # Build students data
        students_data = [
            {
                'student': UserSerializer(allot.student).data,
                'seatNumber': allot.seat_number
            }
            for allot in allotments
        ]
        
        return Response(
            {
                'room': RoomSerializer(room).data,
                'students': students_data
            },
            status=status.HTTP_200_OK
        )
    
    except Room.DoesNotExist:
        return Response(None, status=status.HTTP_200_OK)
