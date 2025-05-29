from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'region'

class Province(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='provinces')

    class Meta:
        db_table = 'province'

class Barangay(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='barangays')

    class Meta:
        db_table = 'barangay'
