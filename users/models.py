from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('trainer', 'Entrenador'),
        ('athlete', 'Deportista'),
        ('guest', 'Invitado'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='guest')

    def __str__(self):
        return f"{self.username} ({self.get_role_display() if hasattr(self, 'get_role_display') else self.role})"
