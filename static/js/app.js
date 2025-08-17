// Student Management System - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize all components
    initializeFormValidation();
    initializeDeleteConfirmations();
    initializeTooltips();
    initializeSearchFilters();
    initializeProgressBars();
    
    // Add loading states for buttons
    initializeLoadingStates();
    
    // Initialize responsive tables
    initializeResponsiveTables();
    
    // Initialize navbar active states
    initializeNavbarActiveStates();
}

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form[novalidate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.value.trim() !== '') {
                    this.classList.add('was-validated');
                }
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('was-validated')) {
                    this.classList.remove('is-invalid', 'is-valid');
                    if (this.checkValidity()) {
                        this.classList.add('is-valid');
                    } else {
                        this.classList.add('is-invalid');
                    }
                }
            });
        });
    });
}

// Delete Confirmations
function initializeDeleteConfirmations() {
    window.confirmDelete = function(itemName, deleteUrl) {
        const modal = document.getElementById('deleteModal');
        const itemNameElement = document.getElementById('deleteItemName');
        const deleteForm = document.getElementById('deleteForm');
        
        if (modal && itemNameElement && deleteForm) {
            itemNameElement.textContent = itemName;
            deleteForm.action = deleteUrl;
            
            const modalInstance = new bootstrap.Modal(modal);
            modalInstance.show();
        } else {
            // Fallback for browsers without modal support
            if (confirm(`Are you sure you want to delete ${itemName}?`)) {
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = deleteUrl;
                document.body.appendChild(form);
                form.submit();
            }
        }
    };
}

// Initialize Bootstrap Tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Search and Filter Functionality
function initializeSearchFilters() {
    const searchInputs = document.querySelectorAll('input[type="search"], input[name="search"]');
    
    searchInputs.forEach(input => {
        // Auto-submit search forms after user stops typing
        let searchTimeout;
        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.form) {
                    this.form.submit();
                }
            }, 500);
        });
        
        // Clear search functionality
        const clearButton = input.parentElement.querySelector('.btn-clear-search');
        if (clearButton) {
            clearButton.addEventListener('click', function() {
                input.value = '';
                input.form.submit();
            });
        }
    });
}

// Animated Progress Bars
function initializeProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBar = entry.target;
                const width = progressBar.style.width;
                progressBar.style.width = '0%';
                
                setTimeout(() => {
                    progressBar.style.width = width;
                    progressBar.style.transition = 'width 0.8s ease-in-out';
                }, 100);
                
                observer.unobserve(progressBar);
            }
        });
    }, observerOptions);
    
    progressBars.forEach(bar => {
        observer.observe(bar);
    });
}

// Loading States for Buttons
function initializeLoadingStates() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                
                const originalText = submitButton.innerHTML;
                submitButton.innerHTML = `
                    <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    Processing...
                `;
                
                // Re-enable button after timeout (fallback)
                setTimeout(() => {
                    submitButton.disabled = false;
                    submitButton.innerHTML = originalText;
                }, 10000);
            }
        });
    });
}

// Responsive Tables
function initializeResponsiveTables() {
    const tables = document.querySelectorAll('.table-responsive table');
    
    tables.forEach(table => {
        // Add mobile-friendly row highlighting
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(row => {
            row.addEventListener('click', function() {
                // Remove previous highlights
                rows.forEach(r => r.classList.remove('table-active'));
                // Add highlight to clicked row
                this.classList.add('table-active');
            });
        });
    });
}

// Utility Functions
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container > .alert') || 
                          document.querySelector('main .container');
    
    if (alertContainer) {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        if (alertContainer.classList.contains('alert')) {
            alertContainer.parentNode.insertBefore(alert, alertContainer.nextSibling);
        } else {
            alertContainer.insertBefore(alert, alertContainer.firstChild);
        }
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }
}

function formatNumber(num, decimals = 0) {
    return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    }).format(num);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    }).format(date);
}

// GPA Calculator Utility
function calculateGPA(grades) {
    const gradePoints = {
        'A+': 4.0, 'A': 4.0, 'A-': 3.7,
        'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7,
        'D+': 1.3, 'D': 1.0, 'D-': 0.7,
        'F': 0.0
    };
    
    if (!grades || grades.length === 0) return 0.0;
    
    let totalPoints = 0;
    let totalCredits = 0;
    
    grades.forEach(grade => {
        const points = gradePoints[grade.letter_grade] || 0;
        const credits = grade.credits || 1;
        totalPoints += points * credits;
        totalCredits += credits;
    });
    
    return totalCredits > 0 ? totalPoints / totalCredits : 0.0;
}

// Auto-uppercase for course codes
document.addEventListener('input', function(e) {
    if (e.target.id === 'code' || e.target.name === 'code') {
        e.target.value = e.target.value.toUpperCase();
    }
});

// Enhanced search functionality for student/course selection
function enhanceSelectElements() {
    const selects = document.querySelectorAll('select.form-select');
    
    selects.forEach(select => {
        // Add search functionality for long lists
        if (select.options.length > 10) {
            select.setAttribute('data-live-search', 'true');
        }
        
        // Add change event listeners
        select.addEventListener('change', function() {
            const event = new CustomEvent('selectChanged', {
                detail: {
                    element: this,
                    value: this.value,
                    text: this.options[this.selectedIndex].text
                }
            });
            document.dispatchEvent(event);
        });
    });
}

// Initialize enhanced selects
document.addEventListener('DOMContentLoaded', enhanceSelectElements);

// Navbar Active States
function initializeNavbarActiveStates() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link-modern');
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        
        // Get the href attribute and compare with current path
        const href = link.getAttribute('href');
        if (href && (currentPath === href || (href !== '/' && currentPath.startsWith(href)))) {
            link.classList.add('active');
        }
    });
}

// Export utilities for use in other scripts
window.SMS = {
    showAlert,
    formatNumber,
    formatDate,
    calculateGPA,
    confirmDelete: window.confirmDelete
};
