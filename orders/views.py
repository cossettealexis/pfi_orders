from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import date
from django.db.models import F, Q
from collections import defaultdict

from core import models
from customers.models import Customer
from products.models import Product
from users.models import User
from users.roles import AgentRole, get_user_role
from .models import Order, OrderProduct, OrderStatus, OrderHistory
from .forms import OrderForm

@login_required
def order_list(request):
    role = get_user_role(request.user)
    if role.can_view_all_orders():
        orders = Order.objects.all()
    elif role.can_view_orders():
        orders = Order.objects.filter(agent=request.user)
    else:
        orders = Order.objects.none()

    search_query = request.GET.get('search', '')
    sort = request.GET.get('sort', 'created_at')
    dir = request.GET.get('dir', 'desc')

    if search_query:
        orders = orders.filter(
            Q(customer__name__icontains=search_query) |
            Q(status__name__icontains=search_query)
        )

    # Map sort keys to model fields
    sort_fields = {
        'id': 'id',
        'customer': 'customer__name',
        'agent': 'agent__username',
        'status': 'status__name',
        'total': 'total_amount',
        'created_at': 'created_at',
        'updated_at': 'updated_at',
    }
    sort_field = sort_fields.get(sort, 'created_at')
    if dir == 'desc':
        sort_field = '-' + sort_field

    orders = orders.order_by(sort_field)
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_history = OrderHistory.objects.filter(order=order).order_by('-timestamp')
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'order_history': order_history,
    })

@login_required
def order_create(request):
    customer_id = request.GET.get('customer_id')
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

            OrderHistory.objects.create(
                order=order,
                user=request.user,
                action="Order created",
                notes=""
            )

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

    return render(request, 'orders/order_form.html', {
        'form': form,
        'agents': agents,
        'customers': customers,
        'products': products,
        'statuses': statuses,
        'logged_in_agent': logged_in_agent,
        'action': 'Add',
        'selected_customer_id': customer_id,
    })

@login_required
def order_edit(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    customer_id = request.GET.get('customer_id')
    role = get_user_role(request.user)

    # Only allow agents to edit if order is pending
    if isinstance(role, AgentRole):
        if not role.can_edit_cancel_order(order):
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
            changes = []
            old_order = Order.objects.get(pk=order.pk)  # get current DB values

            # Compare fields you care about
            if old_order.status_id != int(form.cleaned_data['status'].id):
                changes.append(f"Status: {old_order.status.name} → {form.cleaned_data['status'].name}")
            if old_order.customer_id != int(form.cleaned_data['customer'].id):
                changes.append(f"Customer: {old_order.customer.name} → {form.cleaned_data['customer'].name}")
            if old_order.agent_id != int(form.cleaned_data['agent'].id):
                changes.append(f"Agent: {old_order.agent.username} → {form.cleaned_data['agent'].username}")

            # Build old and new product dicts: {product_id: quantity}
            old_products = {op.product_id: op.quantity for op in old_order.order_products.all()}
            new_products = {}
            product_ids = request.POST.get('products', '').split(',')
            quantities = request.POST.get('quantities', '').split(',')
            for product_id, qty in zip(product_ids, quantities):
                if product_id and qty:
                    new_products[int(product_id)] = int(qty)

            # Find added, removed, and changed products
            product_changes = []
            for pid, qty in new_products.items():
                if pid not in old_products:
                    product = Product.objects.get(id=pid)
                    product_changes.append(f"Added {product.name} (x{qty})")
                elif old_products[pid] != qty:
                    product = Product.objects.get(id=pid)
                    product_changes.append(f"Changed {product.name} quantity: {old_products[pid]} → {qty}")
            for pid, qty in old_products.items():
                if pid not in new_products:
                    product = Product.objects.get(id=pid)
                    product_changes.append(f"Removed {product.name} (was x{qty})")

            if product_changes:
                changes.append("Products/quantities: " + "; ".join(product_changes))

            if not changes:
                messages.info(request, "No changes detected. Nothing was updated.")
                return redirect('order_detail', order_id=order.id)

            # Save the order
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

            # Save history with details
            OrderHistory.objects.create(
                order=order,
                user=request.user,
                action="Order updated",
                notes="; ".join(changes)
            )

            return redirect('order_list')
    else:
        form = OrderForm(instance=order)

    # Pass selected_customer_id to template
    return render(request, 'orders/order_form.html', {
        'order': order,
        'customers': customers,
        'products': products,
        'selected_customer_id': customer_id or (order.customer.id if order.customer else None),
        'agents': agents,
        'statuses': statuses,
        'logged_in_agent': logged_in_agent,
        'action': 'Edit',
    })

@login_required
def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # You may want to add a permission check here using role.can_edit_cancel_order(order)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'orders/order_confirm_delete.html', {'order': order})

@login_required
def order_history(request):
    role = get_user_role(request.user)
    if role.can_view_orders():
        orders = Order.objects.filter(agent=request.user).order_by('-created_at')
    elif role.can_view_all_orders():
        orders = Order.objects.all().order_by('-created_at')
    else:
        orders = Order.objects.none()
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def accept_order(request, order_id):
    role = get_user_role(request.user)
    if not role.can_update_order_status():
        return redirect('order_list')
    order = get_object_or_404(Order, id=order_id)
    order.status = OrderStatus.objects.get(name='Accepted')
    order.save()
    return redirect('order_detail', order_id=order.id)
