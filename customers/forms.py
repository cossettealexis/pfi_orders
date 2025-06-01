from django import forms
from .models import Customer, Province, Barangay
from users.roles import get_user_role

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
        if user:
            role = get_user_role(user)
            # Only show agent's regions if user is agent
            if hasattr(role, 'can_view_customers') and role.can_view_customers() and not role.can_view_all_customers():
                self.fields['region'].queryset = user.regions.all()