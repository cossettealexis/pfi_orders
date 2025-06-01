import uuid
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True, editable=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = f"SKU-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name