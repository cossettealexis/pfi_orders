from django import forms
from .models import User

class UserForm(forms.ModelForm):
    """
    Form for creating and updating User instances.
    Ensures email is required and validates that agents have at least one region assigned.
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'is_active', 'regions']

    def clean(self):
        """
        Custom validation to ensure agents have at least one region assigned.
        """
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        region = cleaned_data.get('regions')
        if role == 'AGENT' and not region:
            self.add_error('regions', 'Region is required for agents.')
        return cleaned_data