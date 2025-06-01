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
});