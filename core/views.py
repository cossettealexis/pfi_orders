from django.http import JsonResponse
from .models import Province, Barangay, Region
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RegionForm

def get_provinces(request):
    region_id = request.GET.get('region_id')
    provinces = Province.objects.filter(region_id=region_id).values('id', 'name')
    return JsonResponse(list(provinces), safe=False)

def get_barangays(request):
    province_id = request.GET.get('province_id')
    barangays = Barangay.objects.filter(province_id=province_id).values('id', 'name')
    return JsonResponse(list(barangays), safe=False)

@login_required
def region_list(request):
    regions = Region.objects.all()
    return render(request, 'core/region/region_list.html', {'regions': regions})

@login_required
def region_add(request):
    if request.method == 'POST':
        form = RegionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('region_list')
    else:
        form = RegionForm()
    return render(request, 'core/region/region_form.html', {'form': form, 'action': 'Add'})

@login_required
def region_edit(request, pk):
    region = get_object_or_404(Region, pk=pk)
    if request.method == 'POST':
        form = RegionForm(request.POST, instance=region)
        if form.is_valid():
            form.save()
            return redirect('region_list')
    else:
        form = RegionForm(instance=region)
    return render(request, 'core/region/region_form.html', {'form': form, 'action': 'Edit'})

@login_required
def region_delete(request, pk):
    region = get_object_or_404(Region, pk=pk)
    if request.method == 'POST':
        region.is_active = False
        region.save()
    return redirect('region_list')
