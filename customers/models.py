from django.db import models
from core.models import Barangay, Province, Region

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    barangay = models.ForeignKey(Barangay, on_delete=models.SET_NULL, null=True, related_name='customers')
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, related_name='customers')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, related_name='customers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customer'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.name
