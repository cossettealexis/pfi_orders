from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('AGENT', 'Agent'),
        ('STAFF', 'Staff'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
