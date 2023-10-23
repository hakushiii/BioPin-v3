// navbar.js

// JavaScript function to create a Bootstrap navbar
function createNavbar() {
    // Create navbar element
    const navbar = document.createElement('nav');
    navbar.classList.add('navbar', 'navbar-expand-lg', 'navbar-dark','bg-dark', 'shadow-sm');
  
    // Create container for navbar content
    const container = document.createElement('div');
    container.classList.add('container');
  
    // Create logo in the center
    const logo = document.createElement('a');
    logo.classList.add('navbar-brand', 'mx-auto','font-weight-bold', 'text-white'); // 'mx-auto' centers the element
    logo.href = '#'; // Replace '#' with the actual link for your logo
    logo.innerText = 'BIOPIN'; // Replace 'Your Logo' with your actual logo text or image
  
    // Add logo to container
    container.appendChild(logo);
  
    // Append container to navbar
    navbar.appendChild(container);
  
    // Add click event to the logo to call goBack() function
    logo.addEventListener('click', goBack);
  
    // Append navbar to the body
    document.body.appendChild(navbar);
  }
  
  // Example goBack() function
  function goBack() {
    window.history.back();
  }
  