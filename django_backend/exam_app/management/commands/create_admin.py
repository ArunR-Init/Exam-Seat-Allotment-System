"""
Django management command to create default admin user.
Replicates the Node.js behavior of creating admin on startup.
"""
from django.core.management.base import BaseCommand
from exam_app.models import User


class Command(BaseCommand):
    help = 'Create default admin user if not exists'

    def handle(self, *args, **options):
        """Create admin user with default credentials."""
        username = 'admin'
        password = 'adminpassword'
        name = 'System Administrator'
        role = 'admin'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Admin user "{username}" already exists')
            )
        else:
            User.objects.create_user(
                username=username,
                password=password,
                name=name,
                role=role,
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created admin user "{username}"')
            )
