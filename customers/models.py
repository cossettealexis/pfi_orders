from django.db import models
from core.models import Region  # Import Region from core

class Customer(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact_number = models.CharField(max_length=20)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='customers')

    def __str__(self):
        return self.name
