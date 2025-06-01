from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from core.models import Region

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Adds role-based access and region assignments for agents.
    """
    ROLE_CHOICES = [
        ('AGENT', 'Agent'),
        ('STAFF', 'Staff'),
        ('ADMIN', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    regions = models.ManyToManyField(Region, related_name='agents', blank=True)  # Agents assigned to regions

    # Use custom related_name to avoid conflicts with Django's default User model
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True
    )

    class Meta:
        db_table = 'auth_user'  # Use the same table as the default User model
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
