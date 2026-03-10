"""
URL configuration for template views (web pages).
"""
from django.urls import path
from . import template_views

urlpatterns = [
    # Public pages
    path('', template_views.home_view, name='home'),
    path('register/', template_views.register_view, name='register'),
    path('login/<str:role>/', template_views.login_view, name='login'),
    path('logout/', template_views.logout_view, name='logout'),
    path('dashboard/', template_views.dashboard_view, name='dashboard'),
    
    # Student pages
    path('student/', template_views.student_dashboard_view, name='student_dashboard'),
    
    # Teacher pages
    path('teacher/', template_views.teacher_dashboard_view, name='teacher_dashboard'),
    
    # Admin pages
    path('admin-dashboard/', template_views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-dashboard/add-teacher/', template_views.add_teacher_view, name='add_teacher'),
    path('admin-dashboard/allot/', template_views.allot_rooms_view, name='allot_rooms'),
]
