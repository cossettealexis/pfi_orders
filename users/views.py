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
    """
    Handle user login. Authenticates and logs in user, redirects to dashboard on success.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid username or password'})
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    """
    Log out the current user and redirect to login page.
    """
    logout(request)
    return redirect('user_login')

@login_required
def dashboard(request):
    """
    Display dashboard with order statistics based on user role.
    """
    if request.user.role == "AGENT":
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
    """
    Display a list of users with search and sorting. Only accessible to users with user management permissions.
    """
    role = get_user_role(request.user)
    if not role.can_manage_users():
        return redirect('dashboard')

    users = User.objects.all()

    search_query = request.GET.get('search', '').strip()
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query)
        )

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
    """
    Handle creation of a new user. Only accessible to users with user management permissions.
    """
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
                user.set_unusable_password()
            user.save()
            form.save_m2m()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'users/user_form.html', {'form': form, 'action': 'Add'})

@login_required
def user_edit(request, pk):
    """
    Handle editing of an existing user. Only accessible to users with user management permissions.
    """
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
    """
    Soft delete a user by setting is_active to False. Only accessible to users with user management permissions.
    """
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
    """
    Display the details of a specific user. Only accessible to users with user management permissions.
    """
    role = get_user_role(request.user)
    if not role.can_manage_users():
        return redirect('dashboard')
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/user_detail.html', {'user': user})
