from django.contrib import admin
from .models import Region, Province, Barangay

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region')
    search_fields = ('name',)
    list_filter = ('region',)

@admin.register(Barangay)
class BarangayAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'province')
    search_fields = ('name',)
    list_filter = ('province',)
