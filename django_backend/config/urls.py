"""
URL configuration for exam_allotment project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('exam_app.urls')),  # API routes
    path('', include('exam_app.template_urls')),  # Web page routes
]
