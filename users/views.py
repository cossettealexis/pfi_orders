from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from orders.models import Order, OrderStatus
from customers.models import Customer

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Username: {username}, Password: {password}")  # Debug output
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(f"Authenticated User: {user}")  # Debug output
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
        else:
            print("Authentication Failed")  # Debug output
            return render(request, 'users/login.html', {'error': 'Invalid username or password'})
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

@login_required
def dashboard(request):
    total_orders = Order.objects.count()  # Total number of orders
    pending_orders = Order.objects.filter(status__name='Pending').count()  # Orders with 'Pending' status
    accepted_orders = Order.objects.filter(status__name='Accepted').count()  # Orders with 'Accepted' status

    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'accepted_orders': accepted_orders,
    }
    return render(request, 'users/dashboard.html', context)
