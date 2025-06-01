from rest_framework import serializers
from customers.models import Customer, Region, Province, Barangay

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'region',
            'province',
            'barangay',
        ]

    def validate(self, data):
        region = data.get('region')
        province = data.get('province')
        barangay = data.get('barangay')

        if province and province.region != region:
            raise serializers.ValidationError("Province does not belong to the selected region.")
        if barangay and barangay.province != province:
            raise serializers.ValidationError("Barangay does not belong to the selected province.")
        return data