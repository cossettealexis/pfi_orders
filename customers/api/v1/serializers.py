from rest_framework import serializers
from customers.models import Customer, Region, Province, Barangay

class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model.
    Includes validation to ensure province and barangay belong to the selected region/province.
    """
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
        """
        Ensure province belongs to region and barangay belongs to province.
        """
        region = data.get('region')
        province = data.get('province')
        barangay = data.get('barangay')

        if province and province.region != region:
            raise serializers.ValidationError("Province does not belong to the selected region.")
        if barangay and barangay.province != province:
            raise serializers.ValidationError("Barangay does not belong to the selected province.")
        return data