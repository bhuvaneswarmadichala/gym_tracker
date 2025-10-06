// FitTrack - Main JavaScript File

$(document).ready(function() {
    console.log('FitTrack initialized successfully!');
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow', function() {
            $(this).remove();
        });
    }, 5000);
    
    // Smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function(e) {
        e.preventDefault();
        var target = $(this.getAttribute('href'));
        if (target.length) {
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 70
            }, 1000);
        }
    });
    
    // Form validation feedback
    $('form').on('submit', function() {
        var submitBtn = $(this).find('button[type="submit"]');
        var originalText = submitBtn.html();
        
        submitBtn.prop('disabled', true);
        submitBtn.html('<span class="loading"></span> Processing...');
        
        // Re-enable after 3 seconds (in case of error)
        setTimeout(function() {
            submitBtn.prop('disabled', false);
            submitBtn.html(originalText);
        }, 3000);
    });
    
    // Tooltip initialization (if using Bootstrap tooltips)
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Add animation to cards on scroll
    function animateOnScroll() {
        $('.feature-card, .card').each(function() {
            var elementTop = $(this).offset().top;
            var elementBottom = elementTop + $(this).outerHeight();
            var viewportTop = $(window).scrollTop();
            var viewportBottom = viewportTop + $(window).height();
            
            if (elementBottom > viewportTop && elementTop < viewportBottom) {
                $(this).addClass('animate__animated animate__fadeInUp');
            }
        });
    }
    
    $(window).on('scroll', animateOnScroll);
    animateOnScroll(); // Run on page load
    
    // Number counter animation for stats
    function animateValue(element, start, end, duration) {
        var range = end - start;
        var current = start;
        var increment = end > start ? 1 : -1;
        var stepTime = Math.abs(Math.floor(duration / range));
        
        var timer = setInterval(function() {
            current += increment;
            $(element).text(current);
            if (current == end) {
                clearInterval(timer);
            }
        }, stepTime);
    }
    
    // Animate stat numbers on dashboard
    if ($('.stat-content h3').length) {
        $('.stat-content h3').each(function() {
            var finalValue = parseInt($(this).text());
            if (!isNaN(finalValue)) {
                $(this).text('0');
                animateValue(this, 0, finalValue, 1500);
            }
        });
    }
    
    // Table row click to highlight
    $('.table-hover tbody tr').on('click', function() {
        $(this).addClass('table-active').siblings().removeClass('table-active');
    });
    
    // Confirm before deleting (if delete functionality is added)
    $('.btn-delete').on('click', function(e) {
        if (!confirm('Are you sure you want to delete this item?')) {
            e.preventDefault();
        }
    });
    
    // Dynamic search/filter for tables
    $('#searchInput').on('keyup', function() {
        var value = $(this).val().toLowerCase();
        $('.table tbody tr').filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });
    
    // Print functionality
    $('.btn-print').on('click', function() {
        window.print();
    });
    
    // Export table to CSV (basic implementation)
    $('.btn-export').on('click', function() {
        var table = $(this).closest('.card').find('table');
        var csv = [];
        
        table.find('tr').each(function() {
            var row = [];
            $(this).find('th, td').each(function() {
                row.push($(this).text().trim());
            });
            csv.push(row.join(','));
        });
        
        var csvContent = csv.join('\n');
        var blob = new Blob([csvContent], { type: 'text/csv' });
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = 'fittrack_data.csv';
        a.click();
    });
    
    // Dark mode toggle (optional feature)
    $('#darkModeToggle').on('click', function() {
        $('body').toggleClass('dark-mode');
        var isDark = $('body').hasClass('dark-mode');
        localStorage.setItem('darkMode', isDark);
    });
    
    // Load dark mode preference
    if (localStorage.getItem('darkMode') === 'true') {
        $('body').addClass('dark-mode');
    }
    
    // Form field auto-save to localStorage (optional)
    $('input, select, textarea').on('change', function() {
        if ($(this).attr('data-autosave')) {
            var key = 'fittrack_' + $(this).attr('name');
            localStorage.setItem(key, $(this).val());
        }
    });
    
    // Restore auto-saved form data
    $('input[data-autosave], select[data-autosave], textarea[data-autosave]').each(function() {
        var key = 'fittrack_' + $(this).attr('name');
        var savedValue = localStorage.getItem(key);
        if (savedValue) {
            $(this).val(savedValue);
        }
    });
    
    // Add loading spinner to AJAX requests
    $(document).ajaxStart(function() {
        $('body').addClass('loading');
    }).ajaxStop(function() {
        $('body').removeClass('loading');
    });
    
    // Success message animation
    $('.alert-success').hide().slideDown('slow');
    
    // Error shake animation
    $('.alert-danger').addClass('animate__animated animate__shakeX');
    
    // Back to top button
    var backToTop = $('<button class="btn btn-primary btn-back-to-top"><i class="fas fa-arrow-up"></i></button>');
    $('body').append(backToTop);
    
    $(window).scroll(function() {
        if ($(this).scrollTop() > 300) {
            backToTop.fadeIn();
        } else {
            backToTop.fadeOut();
        }
    });
    
    backToTop.on('click', function() {
        $('html, body').animate({scrollTop: 0}, 800);
        return false;
    });
    
    // Add CSS for back to top button
    $('<style>')
        .text('.btn-back-to-top { position: fixed; bottom: 20px; right: 20px; display: none; z-index: 999; border-radius: 50%; width: 50px; height: 50px; }')
        .appendTo('head');
});

// Utility Functions

// Format number with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Calculate BMI (if needed)
function calculateBMI(weight, height) {
    return (weight / (height * height)).toFixed(2);
}

// Calculate calories burned estimate
function estimateCalories(exercise, duration, weight = 70) {
    var met = {
        'Running': 9.8,
        'Walking': 3.8,
        'Cycling': 7.5,
        'Swimming': 8.0,
        'HIIT': 12.0,
        'Weight Lifting': 6.0,
        'Yoga': 4.0,
        'Other': 5.0
    };
    
    var metValue = met[exercise] || 5.0;
    return Math.round(metValue * weight * (duration / 60));
}

// Validate email format
function isValidEmail(email) {
    var regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

// Show notification
function showNotification(message, type = 'info') {
    var alertClass = 'alert-' + type;
    var notification = $('<div class="alert ' + alertClass + ' alert-dismissible fade show" role="alert">' +
        message +
        '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>' +
        '</div>');
    
    $('.container').first().prepend(notification);
    
    setTimeout(function() {
        notification.fadeOut('slow', function() {
            $(this).remove();
        });
    }, 5000);
}

// Local storage helper
var Storage = {
    set: function(key, value) {
        localStorage.setItem('fittrack_' + key, JSON.stringify(value));
    },
    get: function(key) {
        var value = localStorage.getItem('fittrack_' + key);
        return value ? JSON.parse(value) : null;
    },
    remove: function(key) {
        localStorage.removeItem('fittrack_' + key);
    },
    clear: function() {
        Object.keys(localStorage).forEach(function(key) {
            if (key.startsWith('fittrack_')) {
                localStorage.removeItem(key);
            }
        });
    }
};

console.log('FitTrack JavaScript loaded successfully!');
