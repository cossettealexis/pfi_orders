from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import OrderForm

@login_required
def order_list(request):
    if request.user.role == 'AGENT':
        orders = Order.objects.filter(agent=request.user)
    elif request.user.role == 'STAFF':
        orders = Order.objects.all()
    else:
        orders = []
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
            order.agent = request.user
            order.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/order_create.html', {'form': form})
