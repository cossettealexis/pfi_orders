from django.db import models

class Region(models.Model):
    """
    Model representing a geographic region.
    """
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'region'
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'

    def __str__(self):
        return self.name


class Province(models.Model):
    """
    Model representing a province within a region.
    """
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='provinces')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'province'
        verbose_name = 'Province'
        verbose_name_plural = 'Provinces'
        unique_together = ('name', 'region')

    def __str__(self):
        return self.name


class Barangay(models.Model):
    """
    Model representing a barangay within a province.
    """
    name = models.CharField(max_length=255)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'barangay'
        verbose_name = 'Barangay'
        verbose_name_plural = 'Barangays'
        unique_together = ('name', 'province')

    def __str__(self):
        return self.name
