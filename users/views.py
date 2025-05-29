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
        orders = Order.objects.filter(agent=request.user)
        customers = Customer.objects.filter(orders__agent=request.user).distinct()
    elif request.user.role == 'STAFF':
        orders = Order.objects.all()
        customers = Customer.objects.all()
    else:
        orders = []
        customers = []
    return render(request, 'users/dashboard.html', {'orders': orders, 'customers': customers})
