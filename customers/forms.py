from django import forms
from .models import Customer, Province, Barangay

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'region', 'province', 'barangay']  # <-- No 'address' here

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'regions'):
            self.fields['region'].queryset = user.regions.all()
        # Prefill province queryset if instance exists
        if self.instance and self.instance.pk:
            region = self.instance.region
            province = self.instance.province
            if region:
                self.fields['province'].queryset = Province.objects.filter(region=region)
            if province:
                self.fields['barangay'].queryset = Barangay.objects.filter(province=province)

        # If POST data is present, update querysets accordingly
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['province'].queryset = Province.objects.filter(region_id=region_id)
            except (ValueError, TypeError):
                pass
        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['barangay'].queryset = Barangay.objects.filter(province_id=province_id)
            except (ValueError, TypeError):
                pass