from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product
from .forms import ProductForm
from users.roles import get_user_role

@login_required
def product_list(request):
    """
    Display a list of products with optional search and sorting.
    Only users with product management permissions can access.
    """
    role = get_user_role(request.user)
    if not role.can_manage_products():
        return redirect('dashboard')

    search_query = request.GET.get('search', '').strip()
    products = Product.objects.all()
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(sku__icontains=search_query)
        )

    sort = request.GET.get('sort', 'name')
    dir_ = request.GET.get('dir', 'asc')
    if sort not in ['name', 'sku', 'description', 'price', 'stock']:
        sort = 'name'
    if dir_ == 'desc':
        sort = '-' + sort
    products = products.order_by(sort)

    return render(request, 'products/product_list.html', {'products': products})

@login_required
def product_add(request):
    """
    Handle creation of a new product.
    Only users with product management permissions can add products.
    """
    role = get_user_role(request.user)
    if not role.can_manage_products():
        return redirect('dashboard')
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Add'})

@login_required
def product_edit(request, pk):
    """
    Handle editing of an existing product.
    Only users with product management permissions can edit products.
    """
    role = get_user_role(request.user)
    if not role.can_manage_products():
        return redirect('dashboard')
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Edit'})

@login_required
def product_delete(request, pk):
    """
    Handle deletion of a product.
    Only users with product management permissions can delete products.
    """
    role = get_user_role(request.user)
    if not role.can_manage_products():
        return redirect('dashboard')
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    # Redirect to detail if not POST (no confirmation page)
    return redirect('product_detail', pk=pk)

@login_required
def product_detail(request, pk):
    """
    Display the details of a specific product.
    Only users with product management permissions can view details.
    """
    role = get_user_role(request.user)
    if not role.can_manage_products():
        return redirect('dashboard')
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})
