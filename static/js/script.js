// TLC Business Solutions - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Mobile Navigation
    initMobileNav();
    
    // Initialize Smooth Scroll
    initSmoothScroll();
    
    // Initialize Animation on Scroll
    initScrollAnimation();
    
    // Initialize Form Validation
    initFormValidation();
    
    // Initialize Flash Message Timeout
    initFlashMessages();
});

// Mobile Navigation Toggle
function initMobileNav() {
    const hamburger = document.querySelector('.hamburger');
    const nav = document.querySelector('nav');
    
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            nav.classList.toggle('active');
            
            // Change hamburger icon
            if (nav.classList.contains('active')) {
                hamburger.innerHTML = '<i class="fas fa-times"></i>';
            } else {
                hamburger.innerHTML = '<i class="fas fa-bars"></i>';
            }
        });
    }
    
    // Close mobile nav when clicking outside
    document.addEventListener('click', function(event) {
        if (nav && nav.classList.contains('active') && !event.target.closest('nav') && event.target !== hamburger) {
            nav.classList.remove('active');
            hamburger.innerHTML = '<i class="fas fa-bars"></i>';
        }
    });
}

// Smooth Scroll for Anchor Links
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                // Close mobile nav if open
                const nav = document.querySelector('nav');
                const hamburger = document.querySelector('.hamburger');
                
                if (nav && nav.classList.contains('active')) {
                    nav.classList.remove('active');
                    hamburger.innerHTML = '<i class="fas fa-bars"></i>';
                }
                
                window.scrollTo({
                    top: targetElement.offsetTop - 80, // Account for fixed header
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Animation on Scroll
function initScrollAnimation() {
    const elements = document.querySelectorAll('.fade-in');
    
    // Initial check for elements in viewport
    checkVisibility(elements);
    
    // Listen for scroll events
    window.addEventListener('scroll', function() {
        checkVisibility(elements);
    });
}

function checkVisibility(elements) {
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150; // How much of the element should be visible
        
        if (elementTop < window.innerHeight - elementVisible) {
            element.classList.add('appear');
        }
    });
}

// Contact Form Validation
function initFormValidation() {
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            let valid = true;
            
            // Reset previous error messages
            document.querySelectorAll('.error-message').forEach(el => el.remove());
            
            // Validate name
            const nameInput = document.getElementById('name');
            if (!nameInput.value.trim()) {
                valid = false;
                showError(nameInput, 'Please enter your name');
            }
            
            // Validate email
            const emailInput = document.getElementById('email');
            if (!isValidEmail(emailInput.value.trim())) {
                valid = false;
                showError(emailInput, 'Please enter a valid email address');
            }
            
            // Validate phone (optional, but must be valid if provided)
            const phoneInput = document.getElementById('phone');
            if (phoneInput.value.trim() && !isValidPhone(phoneInput.value.trim())) {
                valid = false;
                showError(phoneInput, 'Please enter a valid phone number');
            }
            
            // Validate message
            const messageInput = document.getElementById('message');
            if (!messageInput.value.trim()) {
                valid = false;
                showError(messageInput, 'Please enter your message');
            }
            
            if (!valid) {
                e.preventDefault();
            }
        });
    }
}

function showError(inputElement, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.color = '#e74c3c';
    errorDiv.style.fontSize = '0.85rem';
    errorDiv.style.marginTop = '0.25rem';
    errorDiv.textContent = message;
    
    inputElement.parentNode.appendChild(errorDiv);
    inputElement.style.borderColor = '#e74c3c';
}

function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

function isValidPhone(phone) {
    const regex = /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/;
    return regex.test(phone);
}

// Flash Messages
function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        // Automatically remove flash message after 5 seconds
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transform = 'translateX(100%)';
            
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
        
        // Allow user to dismiss message by clicking on it
        message.addEventListener('click', function() {
            message.style.opacity = '0';
            message.style.transform = 'translateX(100%)';
            
            setTimeout(() => {
                message.remove();
            }, 300);
        });
    });
}
