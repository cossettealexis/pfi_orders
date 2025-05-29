from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from orders.models import Order
from customers.models import Customer

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    if request.user.role == 'AGENT':
        # Filter orders based on the agent's assigned regions
        orders = Order.objects.filter(customer__barangay__province__region__in=request.user.regions.all())
    elif request.user.role == 'STAFF':
        orders = Order.objects.all()
    else:
        orders = Order.objects.none()

    total_orders = orders.count()
    pending_orders = orders.filter(status__name='Pending').count()
    accepted_orders = orders.filter(status__name='Accepted').count()

    return render(request, 'users/dashboard.html', {
        'orders': orders,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'accepted_orders': accepted_orders,
    })
