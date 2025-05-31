from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import date

from core import models
from customers.models import Customer
from products.models import Product
from users.models import User
from .models import Order, OrderProduct, OrderStatus
from .forms import OrderForm

@login_required
def order_list(request):
    search_query = request.GET.get('search', '')
    print(f"User Role: {request.user.role}")  # Debug output
    print(f"Is Superuser: {request.user.is_superuser}")  # Debug output

    if request.user.is_superuser:
        orders = Order.objects.all()
    elif request.user.role == 'AGENT':
        orders = Order.objects.filter(agent=request.user)
    elif request.user.role == 'STAFF':
        orders = Order.objects.all()
    else:
        orders = Order.objects.none()

    if search_query:
        orders = orders.filter(customer__name__icontains=search_query)

    # Order by descending created date
    orders = orders.order_by('-created_at')

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
            order.agent = form.cleaned_data.get('agent')
            order.save()

            product_ids = request.POST.get('products', '').split(',')
            quantities = request.POST.get('quantities', '').split(',')
            total = 0
            for product_id, qty in zip(product_ids, quantities):
                try:
                    product = Product.objects.get(id=product_id)
                    quantity = int(qty) if qty.isdigit() else 1
                    OrderProduct.objects.create(order=order, product=product, quantity=quantity)
                    total += product.price * quantity
                except Product.DoesNotExist:
                    print(f"Product with ID {product_id} does not exist.")

            order.total_amount = total
            order.save()

            return redirect('order_list')
        else:
            print(form.errors)  # Debug output to inspect validation errors
    else:
        form = OrderForm()

    # --- Apply agent/staff logic here ---
    if request.user.role == 'AGENT':
        agents = User.objects.filter(id=request.user.id)
        logged_in_agent = request.user
        statuses = OrderStatus.objects.filter(name__in=['Pending', 'Cancelled'])
        customers = Customer.objects.filter(region__in=request.user.regions.all())
    else:
        agents = User.objects.filter(role='AGENT')
        logged_in_agent = None
        statuses = OrderStatus.objects.all()
        customers = Customer.objects.all()
    products = Product.objects.all()
    # ------------------------------------

    return render(request, 'orders/order_create.html', {
        'form': form,
        'agents': agents,
        'customers': customers,
        'products': products,
        'statuses': statuses,
        'logged_in_agent': logged_in_agent,
    })

@login_required
def order_edit(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Only allow agents to edit if order is pending
    if request.user.role == 'AGENT':
        if order.status.name != 'Pending':
            messages.warning(request, "You can only edit orders that are still pending.")
            return redirect('order_detail', order_id=order.id)
        agents = User.objects.filter(id=request.user.id)
        logged_in_agent = request.user
        statuses = OrderStatus.objects.filter(name__in=['Pending', 'Cancelled'])
        customers = Customer.objects.filter(region__in=request.user.regions.all())
    else:
        agents = User.objects.filter(role='AGENT')
        logged_in_agent = None
        statuses = OrderStatus.objects.all()
        customers = Customer.objects.all()

    products = Product.objects.all()

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order.agent = form.cleaned_data.get('agent')
            order.save()

            # --- Handle products and quantities ---
            product_ids = request.POST.get('products', '').split(',')
            quantities = request.POST.get('quantities', '').split(',')

            # Remove existing order products
            order.order_products.all().delete()

            total = 0
            for product_id, qty in zip(product_ids, quantities):
                if not product_id or not qty:
                    continue
                try:
                    product = Product.objects.get(id=product_id)
                    quantity = int(qty) if qty.isdigit() else 1
                    OrderProduct.objects.create(order=order, product=product, quantity=quantity)
                    total += product.price * quantity
                except Product.DoesNotExist:
                    continue

            order.total_amount = total
            order.save()
            # --- End handle products and quantities ---

            return redirect('order_list')
    else:
        form = OrderForm(instance=order)

    return render(request, 'orders/order_edit.html', {
        'order': order,
        'agents': agents,
        'customers': customers,
        'statuses': statuses,
        'products': products,
        'logged_in_agent': logged_in_agent,
    })

@login_required
def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')  # Redirect to the order list after deletion
    return render(request, 'orders/order_confirm_delete.html', {'order': order})

@login_required
def order_history(request):
    if request.user.role == 'AGENT':
        orders = Order.objects.filter(agent=request.user).order_by('-created_at')
    elif request.user.role == 'STAFF':
        orders = Order.objects.all().order_by('-created_at')
    else:
        orders = Order.objects.none()
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def accept_order(request, order_id):
    if request.user.role != 'STAFF':
        return redirect('order_list')
    order = get_object_or_404(Order, id=order_id)
    order.status = OrderStatus.objects.get(name='Accepted')
    order.save()
    return redirect('order_detail', order_id=order.id)
