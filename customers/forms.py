from django import forms
from .models import Customer, Province, Barangay

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'region', 'province', 'barangay']
        error_messages = {
            'name': {'required': 'Name is required.'},
            'email': {'required': 'Email is required.'},
            'region': {'required': 'Region is required.'},
            'province': {'required': 'Province is required.'},
            'barangay': {'required': 'Barangay is required.'},
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Only show agent's regions if user is agent
        if user and getattr(user, 'role', None) == 'AGENT':
            self.fields['region'].queryset = user.regions.all()