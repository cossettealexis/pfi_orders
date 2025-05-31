from django.http import JsonResponse
from .models import Province, Barangay

def get_provinces(request):
    region_id = request.GET.get('region_id')
    provinces = Province.objects.filter(region_id=region_id).values('id', 'name')
    return JsonResponse(list(provinces), safe=False)

def get_barangays(request):
    province_id = request.GET.get('province_id')
    barangays = Barangay.objects.filter(province_id=province_id).values('id', 'name')
    return JsonResponse(list(barangays), safe=False)
