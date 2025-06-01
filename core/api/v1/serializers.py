from rest_framework import serializers
from core.models import Region, Province, Barangay

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'is_active']

class ProvinceSerializer(serializers.ModelSerializer):
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())
    class Meta:
        model = Province
        fields = ['id', 'name', 'region', 'is_active']

class BarangaySerializer(serializers.ModelSerializer):
    province = serializers.PrimaryKeyRelatedField(queryset=Province.objects.all())
    class Meta:
        model = Barangay
        fields = ['id', 'name', 'province', 'is_active']