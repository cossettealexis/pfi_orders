from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'barangay')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('barangay',)
