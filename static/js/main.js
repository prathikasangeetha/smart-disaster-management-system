/* Smart Disaster Management & Alert System - Client JavaScript */

document.addEventListener('DOMContentLoaded', function () {
    // Initialize Bootstrap tooltips & popovers
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-fill current date-time on disaster report form if field is blank
    const dateTimeInput = document.getElementById('date_time');
    if (dateTimeInput && !dateTimeInput.value) {
        const now = new Date();
        now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
        dateTimeInput.value = now.toISOString().slice(0, 16);
    }

    // Geolocation helper on report form
    const btnGetLocation = document.getElementById('btn-get-location');
    if (btnGetLocation) {
        btnGetLocation.addEventListener('click', function () {
            if ("geolocation" in navigator) {
                btnGetLocation.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> Detecting...';
                btnGetLocation.disabled = true;

                navigator.geolocation.getCurrentPosition(
                    function (position) {
                        document.getElementById('latitude').value = position.coords.latitude.toFixed(6);
                        document.getElementById('longitude').value = position.coords.longitude.toFixed(6);
                        
                        btnGetLocation.innerHTML = '<i class="fas fa-check me-1"></i> Located!';
                        btnGetLocation.classList.remove('btn-outline-secondary');
                        btnGetLocation.classList.add('btn-success');
                        
                        setTimeout(() => {
                            btnGetLocation.innerHTML = '<i class="fas fa-map-marker-alt me-1"></i> Auto Detect GPS';
                            btnGetLocation.disabled = false;
                        }, 3000);
                    },
                    function (error) {
                        alert('Geolocation failed: ' + error.message);
                        btnGetLocation.innerHTML = '<i class="fas fa-map-marker-alt me-1"></i> Auto Detect GPS';
                        btnGetLocation.disabled = false;
                    }
                );
            } else {
                alert('Geolocation is not supported by your browser.');
            }
        });
    }

    // Interactive Checklist for Guidelines page
    const checklistItems = document.querySelectorAll('.checklist-item');
    if (checklistItems.length > 0) {
        checklistItems.forEach(item => {
            const itemId = item.getAttribute('data-id');
            const savedState = localStorage.getItem('chk_' + itemId);
            if (savedState === 'checked') {
                item.checked = true;
                item.nextElementSibling.classList.add('text-decoration-line-through', 'text-muted');
            }

            item.addEventListener('change', function () {
                if (this.checked) {
                    localStorage.setItem('chk_' + itemId, 'checked');
                    this.nextElementSibling.classList.add('text-decoration-line-through', 'text-muted');
                } else {
                    localStorage.removeItem('chk_' + itemId);
                    this.nextElementSibling.classList.remove('text-decoration-line-through', 'text-muted');
                }
            });
        });
    }
});
