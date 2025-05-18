from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Create default users for testing'

    def handle(self, *args, **kwargs):
        users_data = [
            {'username': 'admin', 'email': 'admin@example.com', 'password': 'adminpass', 'role': 'admin'},
            {'username': 'trainer', 'email': 'trainer@example.com', 'password': 'trainerpass', 'role': 'trainer'},
            {'username': 'athlete', 'email': 'athlete@example.com', 'password': 'athletepass', 'role': 'athlete'},
            {'username': 'guest', 'email': 'guest@example.com', 'password': 'guestpass', 'role': 'guest'},
        ]

        for user_data in users_data:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    role=user_data['role']
                )
                self.stdout.write(self.style.SUCCESS(f"Created user {user.username} with role {user.role}"))
            else:
                self.stdout.write(self.style.WARNING(f"User {user_data['username']} already exists"))
