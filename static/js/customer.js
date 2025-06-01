// --- Modal functions: must be global ---
function openCustomerModal(deleteUrl) {
    const modal = document.getElementById('customer-delete-modal');
    const deleteForm = document.getElementById('customer-delete-form');
    deleteForm.action = deleteUrl;
    modal.style.display = 'flex';
}
function closeCustomerModal() {
    var modal = document.getElementById('customer-delete-modal');
    var form = document.getElementById('customer-delete-form');
    if (modal) modal.style.display = 'none';
    if (form) form.action = '';
}
window.onclick = function(event) {
    var modal = document.getElementById('customer-delete-modal');
    if (event.target == modal) {
        closeCustomerModal();
    }
};

// --- Form validation and dynamic select logic ---
document.addEventListener('DOMContentLoaded', function() {
    var regionSelect = document.getElementById('id_region');
    var provinceSelect = document.getElementById('id_province');
    var barangaySelect = document.getElementById('id_barangay');

    if(regionSelect) {
        regionSelect.addEventListener('change', function() {
            var regionId = this.value;
            provinceSelect.innerHTML = '<option value="">Select a Province</option>';
            barangaySelect.innerHTML = '<option value="">Select a Barangay</option>';
            if(regionId) {
                fetch('/core/ajax/get_provinces/?region_id=' + regionId)
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(function(province) {
                            var option = document.createElement('option');
                            option.value = province.id;
                            option.text = province.name;
                            provinceSelect.add(option);
                        });
                    });
            }
        });
    }

    if(provinceSelect) {
        provinceSelect.addEventListener('change', function() {
            var provinceId = this.value;
            barangaySelect.innerHTML = '<option value="">Select a Barangay</option>';
            if(provinceId) {
                fetch('/core/ajax/get_barangays/?province_id=' + provinceId)
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(function(barangay) {
                            var option = document.createElement('option');
                            option.value = barangay.id;
                            option.text = barangay.name;
                            barangaySelect.add(option);
                        });
                    });
            }
        });
    }

    // Only validate on the customer add/edit form, not the modal
    const form = document.querySelector('form[action=""]') || document.querySelector('form:not(#customer-delete-form)');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        let error = '';
        if (!form.name.value.trim()) {
            error = 'Name is required.';
        } else if (!form.email.value.trim()) {
            error = 'Email is required.';
        } else if (!form.region.value) {
            error = 'Region is required.';
        } else if (!form.province.value) {
            error = 'Province is required.';
        } else if (!form.barangay.value) {
            error = 'Barangay is required.';
        }

        if (error) {
            const errorDiv = document.getElementById('form-error');
            if (errorDiv) errorDiv.textContent = error;
            e.preventDefault();
        }
    });
});