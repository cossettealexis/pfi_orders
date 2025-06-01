from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from orders.models import Order, OrderStatus
from customers.models import Customer
from .models import User
from .forms import UserForm
from users.roles import get_user_role

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
    role = get_user_role(request.user)

    # Use the helper to check if the user is an agent
    if hasattr(role, "name") and role.name == "AGENT":
        orders = Order.objects.filter(agent=request.user)
    else:
        orders = Order.objects.all()

    context = {
        'total_orders': orders.count(),
        'pending_orders': orders.filter(status__name='Pending').count(),
        'accepted_orders': orders.filter(status__name='Accepted').count(),
        'cancelled_orders': orders.filter(status__name='Cancelled').count(),
        'delivered_orders': orders.filter(status__name='Delivered').count(),
        'rejected_orders': orders.filter(status__name='Rejected').count(),
        'dispatched_orders': orders.filter(status__name='Dispatched').count(),
        'orders_by_status': {
            'Pending': orders.filter(status__name='Pending'),
            'Accepted': orders.filter(status__name='Accepted'),
            'Cancelled': orders.filter(status__name='Cancelled'),
            'Delivered': orders.filter(status__name='Delivered'),
            'Rejected': orders.filter(status__name='Rejected'),
            'Dispatched': orders.filter(status__name='Dispatched'),
        }
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def user_list(request):
    role = get_user_role(request.user)
    if not role.can_manage_users():
        return redirect('dashboard')

    users = User.objects.all()

    # --- Searching ---
    search_query = request.GET.get('search', '').strip()
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    # --- Sorting ---
    sort = request.GET.get('sort', 'username')
    dir = request.GET.get('dir', 'asc')
    if sort not in ['username', 'email', 'role', 'is_active']:
        sort = 'username'
    if dir == 'desc':
        sort = '-' + sort
    users = users.order_by('username')

    return render(request, 'users/user_list.html', {'users': users})

@login_required
def user_add(request):
    role = get_user_role(request.user)
    if not role.can_manage_users():
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = request.POST.get('password')
            if raw_password:
                user.set_password(raw_password)
            else:
                # Set a random unusable password if not provided
                user.set_unusable_password()
            user.save()
            form.save_m2m()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'users/user_form.html', {'form': form, 'action': 'Add'})

@login_required
def user_edit(request, pk):
    role = get_user_role(request.user)
    if not role.can_manage_users():
        return redirect('dashboard')
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'users/user_form.html', {'form': form, 'action': 'Edit'})

@login_required
def user_delete(request, pk):
    role = get_user_role(request.user)
    if not role.can_manage_users():
        return redirect('dashboard')
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.is_active = False
        user.save()
        return redirect('user_list')
    return redirect('user_list')

@login_required
def user_detail(request, pk):
    role = get_user_role(request.user)
    if not role.can_manage_users():
        return redirect('dashboard')
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/user_detail.html', {'user': user})
