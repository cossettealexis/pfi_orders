from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Customer
from .forms import CustomerForm

@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, user=request.user)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.region = request.user.regions.first()  # or let agent pick from their regions
            customer.save()
            return redirect('order_create')
    else:
        form = CustomerForm(user=request.user)
    return render(request, 'customers/customer_form.html', {'form': form, 'action': 'Add'})

@login_required
def customer_edit(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.user.role != 'AGENT' or customer.region not in request.user.regions.all():
        return redirect('order_list')
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('order_create')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {'form': form, 'action': 'Edit'})
