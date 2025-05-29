from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'region'
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'

    def __str__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='provinces')

    class Meta:
        db_table = 'province'
        verbose_name = 'Province'
        verbose_name_plural = 'Provinces'
        unique_together = ('name', 'region')

    def __str__(self):
        return self.name


class Barangay(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='barangays')

    class Meta:
        db_table = 'barangay'
        verbose_name = 'Barangay'
        verbose_name_plural = 'Barangays'
        unique_together = ('name', 'province')

    def __str__(self):
        return self.name
