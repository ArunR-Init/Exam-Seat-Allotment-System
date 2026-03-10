"""
URL configuration for exam_app.
Mapping all API endpoints from the Node.js version.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Authentication routes
    path('auth/register-student', views.register_student, name='register_student'),
    path('auth/login', views.login_user, name='login'),
    path('auth/logout', views.logout_user, name='logout'),
    path('auth/me', views.get_me, name='get_me'),
    
    # Admin routes
    path('admin/students', views.get_students, name='get_students'),
    path('admin/teachers', views.get_teachers, name='get_teachers'),
    path('admin/teachers', views.add_teacher, name='add_teacher'),  # POST to same URL
    path('admin/allot', views.allot_rooms, name='allot_rooms'),
    
    # Student routes
    path('student/allotment', views.get_student_allotment, name='get_student_allotment'),
    
    # Teacher routes
    path('teacher/room', views.get_teacher_room, name='get_teacher_room'),
]
