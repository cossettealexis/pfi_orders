function openModal(deleteUrl) {
    const modal = document.getElementById('deleteModal');
    const deleteForm = document.getElementById('deleteForm');
    deleteForm.action = deleteUrl;
    modal.style.display = 'flex';
}

function closeModal() {
    const modal = document.getElementById('deleteModal');
    modal.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    // --- Shared logic for create/edit ---
    const createForm = document.getElementById('order-create-form');
    const editForm = document.getElementById('order-edit-form');
    const isEdit = !!editForm;
    const form = createForm || editForm;
    if (!form) return;

    let selectedProducts = [];

    // Prefill for edit page
    if (isEdit) {
        const dataDiv = document.getElementById('order-edit-data');
        if (dataDiv) {
            try {
                selectedProducts = JSON.parse(dataDiv.getAttribute('data-products'));
            } catch (e) {
                selectedProducts = [];
            }
        }
    }

    const productSelect = document.getElementById('products');
    const productList = document.getElementById('product-list');
    const totalAmountInput = document.getElementById('total_amount');
    const formProducts = document.getElementById('form-products');
    const formQuantities = document.getElementById('form-quantities');

    function renderProductList() {
        if (!productList) return;
        productList.innerHTML = '';
        if (selectedProducts.length === 0) {
            const emptyItem = document.createElement('li');
            emptyItem.textContent = 'No product selected';
            emptyItem.style.color = '#888';
            productList.appendChild(emptyItem);
            return;
        }
        selectedProducts.forEach((product, idx) => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span>${product.name} (₱${product.price})</span>
                <input type="number" min="1" value="${product.quantity}" data-idx="${idx}" class="product-qty-input" style="width:60px; margin-left:8px; margin-right:8px;">
                <button type="button" class="remove-product-btn" data-idx="${idx}" style="margin-left:4px;">Remove</button>
            `;
            productList.appendChild(li);
        });
        updateTotal();
    }

    function updateTotal() {
        let total = 0;
        selectedProducts.forEach(product => {
            total += product.price * product.quantity;
        });
        if (totalAmountInput) totalAmountInput.value = total.toFixed(2);
        if (formProducts) formProducts.value = selectedProducts.map(p => p.id).join(',');
        if (formQuantities) formQuantities.value = selectedProducts.map(p => p.quantity).join(',');
    }

    // Add product from dropdown
    if (productSelect) {
        productSelect.addEventListener('change', function() {
            const selectedOption = productSelect.options[productSelect.selectedIndex];
            const prodId = selectedOption.value;
            if (!prodId) return;
            // Prevent duplicate
            if (selectedProducts.some(p => p.id == prodId)) return;
            const prodName = selectedOption.getAttribute('data-name');
            const prodPrice = parseFloat(selectedOption.getAttribute('data-price'));
            selectedProducts.push({ id: prodId, name: prodName, price: prodPrice, quantity: 1 });
            renderProductList();
        });
    }

    // Delegate quantity change and remove
    if (productList) {
        productList.addEventListener('input', function(e) {
            if (e.target.classList.contains('product-qty-input')) {
                const idx = e.target.getAttribute('data-idx');
                let qty = parseInt(e.target.value, 10);
                if (isNaN(qty) || qty < 1) qty = 1;
                selectedProducts[idx].quantity = qty;
                renderProductList();
            }
        });
        productList.addEventListener('click', function(e) {
            if (e.target.classList.contains('remove-product-btn')) {
                const idx = e.target.getAttribute('data-idx');
                selectedProducts.splice(idx, 1);
                renderProductList();
            }
        });
    }

    // Form validation
    form.addEventListener('submit', function(e) {
        showError('');
        const agent = document.getElementById('agent').value;
        if (!agent) {
            showError('Agent is required.');
            e.preventDefault();
            return false;
        }
        const customer = document.getElementById('customer').value;
        if (!customer) {
            showError('Customer is required.');
            e.preventDefault();
            return false;
        }
        if (selectedProducts.length === 0) {
            showError('Please select at least one product.');
            e.preventDefault();
            return false;
        }
        for (const product of selectedProducts) {
            if (!product.quantity || product.quantity < 1) {
                showError('Quantity for all products must be at least 1.');
                e.preventDefault();
                return false;
            }
        }
    });

    function showError(message) {
        let errorDiv = document.getElementById('form-error');
        if (errorDiv) errorDiv.textContent = message;
    }

    // Initial render for both create and edit
    renderProductList();
    updateTotal();

    // Prefill products if editing (works for unified form)
    const dataDiv = document.getElementById('order-edit-data');
    if (dataDiv) {
        try {
            selectedProducts = JSON.parse(dataDiv.getAttribute('data-products'));
        } catch (e) {
            selectedProducts = [];
        }
    }
});