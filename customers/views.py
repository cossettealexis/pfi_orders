from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Customer
from .forms import CustomerForm
from django.urls import reverse
from users.roles import get_user_role

@login_required
def customer_create(request):
    next_param = request.GET.get('next') or request.POST.get('next')
    if next_param == 'order_create':
        next_url = reverse('order_create')
    elif next_param and next_param.startswith('order_edit:'):
        order_id = next_param.split(':')[1]
        next_url = reverse('order_edit', args=[order_id])
    else:
        next_url = reverse('customer_list')

    if request.method == 'POST':
        form = CustomerForm(request.POST, user=request.user)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.region = request.user.regions.first()
            customer.save()
            if next_param == 'order_create':
                return redirect(f"{reverse('order_create')}?customer_id={customer.id}")
            elif next_param and next_param.startswith('order_edit:'):
                order_id = next_param.split(':')[1]
                return redirect(f"{reverse('order_edit', args=[order_id])}?customer_id={customer.id}")
            else:
                return redirect('customer_list')
    else:
        form = CustomerForm(user=request.user)
    return render(request, 'customers/customer_form.html', {
        'form': form,
        'action': 'Add',
        'next': next_param,
        'next_url': next_url,
        'customer_list_url': reverse('customer_list'),
    })

@login_required
def customer_edit(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    role = get_user_role(request.user)
    if not role.can_add_edit_customer(customer):
        return redirect('customer_list')
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer, user=request.user)
    next_url = request.GET.get('next') or reverse('customer_list')
    return render(request, 'customers/customer_form.html', {
        'form': form,
        'customer': customer,
        'action': 'Edit',
        'next_url': next_url,
    })

@login_required
def customer_list(request):
    role = get_user_role(request.user)
    if role.can_view_all_customers():
        customers = Customer.objects.all()
    elif role.can_view_customers():
        customers = Customer.objects.filter(region__in=request.user.regions.all())
    else:
        customers = Customer.objects.none()

    sort = request.GET.get('sort', 'created_at')
    direction = request.GET.get('dir', 'desc')
    search = request.GET.get('search', '').strip()
    sort_map = {
        'name': 'name',
        'email': 'email',
        'phone': 'phone',
        'created_at': 'created_at',
        'address': 'barangay__name',
    }
    sort_field = sort_map.get(sort, 'created_at')
    order_by = sort_field if direction == 'asc' else f'-{sort_field}'

    # Apply search filter (now includes address fields)
    if search:
        customers = customers.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search) |
            Q(barangay__name__icontains=search) |
            Q(province__name__icontains=search) |
            Q(region__name__icontains=search)
        )

    customers = customers.order_by(order_by)
    return render(request, 'customers/customer_list.html', {'customers': customers})

@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    return render(request, 'customers/customer_detail.html', {'customer': customer})

@login_required
def customer_delete(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    role = get_user_role(request.user)
    if not role.can_add_edit_any_customer():
        return redirect('customer_list')
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})
