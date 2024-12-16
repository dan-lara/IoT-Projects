// main.js - Dark Mode Functionality

document.addEventListener('DOMContentLoaded', () => {
    // Get dark mode toggle and body elements
    const darkModeToggle = document.getElementById('darkModeToggle');
    const body = document.body;

    // Check for saved dark mode preference
    const savedDarkMode = localStorage.getItem('darkMode');

    // Set initial dark mode state
    if (savedDarkMode === 'enabled') {
        body.classList.add('dark-mode');
        darkModeToggle.checked = true;
    }

    // Dark mode toggle event listener
    darkModeToggle.addEventListener('change', () => {
        if (darkModeToggle.checked) {
            // Enable dark mode
            body.classList.add('dark-mode');
            localStorage.setItem('darkMode', 'enabled');
        } else {
            // Disable dark mode
            body.classList.remove('dark-mode');
            localStorage.setItem('darkMode', null);
        }
    });
});