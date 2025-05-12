document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Add confirmation for delete actions
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });
    
    // Image preview for file inputs
    const imageInputs = document.querySelectorAll('input[type="file"][accept="image/*"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function() {
            const previewContainer = this.nextElementSibling;
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    if (!previewContainer) {
                        const newPreview = document.createElement('div');
                        newPreview.className = 'mt-2';
                        newPreview.innerHTML = '<small>New image preview:</small><br>' + 
                            '<img src="' + e.target.result + '" class="img-thumbnail mt-1" style="max-height: 100px;">';
                        input.parentNode.insertBefore(newPreview, input.nextSibling);
                    } else {
                        const img = previewContainer.querySelector('img');
                        if (img) {
                            img.src = e.target.result;
                        } else {
                            previewContainer.innerHTML = '<small>New image preview:</small><br>' + 
                                '<img src="' + e.target.result + '" class="img-thumbnail mt-1" style="max-height: 100px;">';
                        }
                    }
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    });
});