from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import date

from core import models
from customers.models import Customer
from products.models import Product
from users.models import User
from .models import Order, OrderProduct
from .forms import OrderForm

@login_required
def order_list(request):
    search_query = request.GET.get('search', '')
    print(f"User Role: {request.user.role}")  # Debug output
    print(f"Is Superuser: {request.user.is_superuser}")  # Debug output

    if request.user.is_superuser:
        # Superuser can see all orders
        orders = Order.objects.all()
    elif request.user.role == 'AGENT':
        # Filter orders by agent
        orders = Order.objects.filter(agent=request.user)
    elif request.user.role == 'STAFF':
        # Staff can see all orders
        orders = Order.objects.all()
    else:
        # Return an empty QuerySet for invalid roles
        orders = Order.objects.none()

    if search_query:
        # Apply search filter
        orders = orders.filter(customer__name__icontains=search_query)

    print(f"Orders QuerySet: {orders}")  # Debug output

    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            # Assign the selected agent from the form
            order.agent = form.cleaned_data.get('agent')
            order.save()

            # Save selected products
            product_ids = request.POST.getlist('products')  # Updated field name
            for product_id in product_ids:
                product = Product.objects.get(id=product_id)
                OrderProduct.objects.create(order=order, product=product, quantity=1)  # Default quantity

            return redirect('order_list')  # Redirect to the order list page
    else:
        form = OrderForm()
    
    # Fetch agents, customers, and products
    agents = User.objects.filter(role='AGENT')
    customers = Customer.objects.all()
    products = Product.objects.all()  # Fetch all products

    return render(request, 'orders/order_create.html', {
        'form': form,
        'agents': agents,
        'customers': customers,
        'products': products,
    })

@login_required
def order_edit(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')  # Redirect to the order list after editing
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/order_edit.html', {'form': form, 'order': order})

@login_required
def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')  # Redirect to the order list after deletion
    return render(request, 'orders/order_confirm_delete.html', {'order': order})
