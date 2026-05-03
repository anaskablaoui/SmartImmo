// Basic utility functions for the frontend

document.addEventListener('DOMContentLoaded', () => {
    // Highlight the active nav link based on current URL
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (currentPath.includes(href) && href !== '#') {
            link.classList.add('active');
        }
    });

    // Handle form submissions to prevent page reload for the demo
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            // For the login form
            if (form.id === 'loginForm') {
                e.preventDefault();
                // Simple redirect to home page for demo purposes
                window.location.href = 'home.html';
            } 
            // For other forms (maintenance)
            else {
                e.preventDefault();
                alert('Form submitted successfully! (This is a frontend demo)');
                form.reset();
            }
        });
    });
});
