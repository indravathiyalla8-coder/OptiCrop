/* OptiCrop JavaScript Logic and Validations */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const inputs = document.querySelectorAll('.form-control');
    
    // Limits definition
    const LIMITS = {
        'N': { min: 0, max: 150, name: 'Nitrogen' },
        'P': { min: 5, max: 150, name: 'Phosphorus' },
        'K': { min: 5, max: 220, name: 'Potassium' },
        'temperature': { min: 0, max: 50, name: 'Temperature' },
        'humidity': { min: 10, max: 100, name: 'Humidity' },
        'ph': { min: 3.5, max: 10.0, name: 'pH' },
        'rainfall': { min: 20, max: 300, name: 'Rainfall' }
    };

    // Real-time Validation and Feedback
    inputs.forEach(input => {
        const id = input.id;
        if (LIMITS[id]) {
            // Create validator feedback element if it doesn't exist
            let feedback = input.nextElementSibling;
            if (!feedback || !feedback.classList.contains('validation-feedback')) {
                feedback = document.createElement('div');
                feedback.className = 'validation-feedback text-danger mt-1 small';
                feedback.style.display = 'none';
                input.parentNode.appendChild(feedback);
            }
            
            // Add helper label with expected range below input
            let rangeLabel = document.createElement('div');
            rangeLabel.className = 'text-muted small mt-1';
            rangeLabel.style.fontSize = '0.8rem';
            rangeLabel.innerHTML = `Recommended Range: ${LIMITS[id].min} to ${LIMITS[id].max}`;
            input.parentNode.appendChild(rangeLabel);

            input.addEventListener('input', () => {
                validateField(input, LIMITS[id], feedback);
            });
        }
    });

    function validateField(input, limits, feedback) {
        const value = parseFloat(input.value);
        
        if (input.value.trim() === '') {
            showError(input, feedback, 'This field is required.');
            return false;
        }
        
        if (isNaN(value)) {
            showError(input, feedback, 'Please enter a valid numeric value.');
            return false;
        }
        
        if (value < limits.min || value > limits.max) {
            showError(input, feedback, `${limits.name} must be between ${limits.min} and ${limits.max}.`);
            return false;
        }
        
        showSuccess(input, feedback);
        return true;
    }

    function showError(input, feedback, message) {
        input.classList.remove('is-valid');
        input.classList.add('is-invalid');
        feedback.textContent = message;
        feedback.style.display = 'block';
    }

    function showSuccess(input, feedback) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        feedback.style.display = 'none';
    }

    // Form Submit Event Handler
    if (form) {
        form.addEventListener('submit', function(event) {
            let isValid = true;
            
            inputs.forEach(input => {
                const id = input.id;
                if (LIMITS[id]) {
                    const feedback = input.parentNode.querySelector('.validation-feedback');
                    const fieldValid = validateField(input, LIMITS[id], feedback);
                    if (!fieldValid) {
                        isValid = false;
                    }
                }
            });

            if (!isValid) {
                event.preventDefault();
                event.stopPropagation();
                // Scroll to the first invalid element
                const firstInvalid = document.querySelector('.is-invalid');
                if (firstInvalid) {
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            } else {
                // Add loading spinner animation to submit button
                const btn = form.querySelector('button[type="submit"]');
                btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Analyzing Soil & Environment...';
                btn.disabled = true;
            }
        });
        
        // Reset button handling
        form.addEventListener('reset', function() {
            inputs.forEach(input => {
                input.classList.remove('is-valid', 'is-invalid');
                const feedback = input.parentNode.querySelector('.validation-feedback');
                if (feedback) feedback.style.display = 'none';
            });
        });
    }

    // Results Gauge Animation
    const gaugeFill = document.querySelector('.gauge-fill');
    if (gaugeFill) {
        const score = parseFloat(gaugeFill.getAttribute('data-score')) || 0;
        // Total circumference of circle = 2 * PI * r = 2 * 3.14159 * 70 = 440
        const circumference = 440;
        const offset = circumference - (score / 100) * circumference;
        
        setTimeout(() => {
            gaugeFill.style.strokeDashoffset = offset;
        }, 300);
    }
});
