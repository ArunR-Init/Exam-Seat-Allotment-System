"""
Django admin configuration for the Exam Allotment System.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Room, Allotment


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for User model."""
    list_display = ['username', 'name', 'role', 'is_active']
    list_filter = ['role', 'is_active']
    search_fields = ['username', 'name']
    ordering = ['username']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'role', 'password', 'is_active', 'is_staff'),
        }),
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Admin configuration for Room model."""
    list_display = ['name', 'teacher', 'get_student_count']
    search_fields = ['name', 'teacher__name']
    list_filter = ['teacher']
    
    def get_student_count(self, obj):
        return obj.allotments.count()
    get_student_count.short_description = 'Students'


@admin.register(Allotment)
class AllotmentAdmin(admin.ModelAdmin):
    """Admin configuration for Allotment model."""
    list_display = ['student', 'room', 'seat_number']
    search_fields = ['student__username', 'student__name', 'room__name']
    list_filter = ['room']
    ordering = ['room', 'seat_number']
