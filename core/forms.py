from django import forms
from .models import Region, Barangay, Province

class RegionForm(forms.ModelForm):
    """
    Form for creating and updating Region instances.
    """
    class Meta:
        model = Region
        fields = ['name']

class BarangayForm(forms.ModelForm):
    """
    Form for creating and updating Barangay instances.
    """
    class Meta:
        model = Barangay
        fields = ['name', 'province']

class ProvinceForm(forms.ModelForm):
    """
    Form for creating and updating Province instances.
    """
    class Meta:
        model = Province
        fields = ['name', 'region']