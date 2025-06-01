from django import forms
from .models import Region, Barangay, Province

class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name']

class BarangayForm(forms.ModelForm):
    class Meta:
        model = Barangay
        fields = ['name', 'province']

class ProvinceForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = ['name', 'region']