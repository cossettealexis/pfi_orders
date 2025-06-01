from django.http import JsonResponse
from .models import Province, Barangay, Region
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RegionForm, BarangayForm, ProvinceForm

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
    sort = request.GET.get('sort', 'name')  # default to 'name'
    dir = request.GET.get('dir', 'asc')
    allowed_sorts = ['id', 'name', 'is_active']
    if sort not in allowed_sorts:
        sort = 'name'
    order = sort if dir == 'asc' else f'-{sort}'
    regions = Region.objects.order_by(order)
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

@login_required
def barangay_list(request):
    sort = request.GET.get('sort', 'name')  # default to 'name'
    dir = request.GET.get('dir', 'asc')
    allowed_sorts = ['id', 'name', 'province__name', 'is_active']
    if sort not in allowed_sorts:
        sort = 'name'
    order = sort if dir == 'asc' else f'-{sort}'
    barangays = Barangay.objects.select_related('province').order_by(order)
    return render(request, 'core/barangay/barangay_list.html', {'barangays': barangays})

@login_required
def barangay_add(request):
    if request.method == 'POST':
        form = BarangayForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('barangay_list')
    else:
        form = BarangayForm()
    return render(request, 'core/barangay/barangay_form.html', {'form': form, 'action': 'Add'})

@login_required
def barangay_edit(request, pk):
    barangay = get_object_or_404(Barangay, pk=pk)
    if request.method == 'POST':
        form = BarangayForm(request.POST, instance=barangay)
        if form.is_valid():
            form.save()
            return redirect('barangay_list')
    else:
        form = BarangayForm(instance=barangay)
    return render(request, 'core/barangay/barangay_form.html', {'form': form, 'action': 'Edit'})

@login_required
def barangay_delete(request, pk):
    barangay = get_object_or_404(Barangay, pk=pk)
    if request.method == 'POST':
        barangay.is_active = False
        barangay.save()
    return redirect('barangay_list')

@login_required
def province_list(request):
    sort = request.GET.get('sort', 'name')  # default to 'name'
    dir = request.GET.get('dir', 'asc')
    allowed_sorts = ['id', 'name', 'region__name', 'is_active']
    if sort not in allowed_sorts:
        sort = 'name'
    order = sort if dir == 'asc' else f'-{sort}'
    provinces = Province.objects.select_related('region').order_by(order)
    return render(request, 'core/province/province_list.html', {'provinces': provinces})

@login_required
def province_add(request):
    if request.method == 'POST':
        form = ProvinceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('province_list')
    else:
        form = ProvinceForm()
    return render(request, 'core/province/province_form.html', {'form': form, 'action': 'Add'})

@login_required
def province_edit(request, pk):
    province = get_object_or_404(Province, pk=pk)
    if request.method == 'POST':
        form = ProvinceForm(request.POST, instance=province)
        if form.is_valid():
            form.save()
            return redirect('province_list')
    else:
        form = ProvinceForm(instance=province)
    return render(request, 'core/province/province_form.html', {'form': form, 'action': 'Edit'})

@login_required
def province_delete(request, pk):
    province = get_object_or_404(Province, pk=pk)
    if request.method == 'POST':
        province.is_active = False
        province.save()
    return redirect('province_list')
