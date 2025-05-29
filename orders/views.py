from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from core import models
from .models import Order
from .forms import OrderForm

@login_required
def order_list(request):
    search_query = request.GET.get('search', '')
    if request.user.role == 'AGENT':
        orders = Order.objects.filter(agent=request.user)
    elif request.user.role == 'STAFF':
        orders = Order.objects.all()
    else:
        orders = []

    if search_query:
        orders = orders.filter(
            models.Q(customer__name__icontains=search_query) |
            models.Q(status__name__icontains=search_query)
        )

    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'orders/order_list.html', {'orders': page_obj})

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
            order.agent = request.user
            order.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/order_create.html', {'form': form})
