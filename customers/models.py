from django.db import models
from core.models import Region, Province, Barangay

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='customers')
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='customers')
    barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE, related_name='customers')
    address = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'customer'
