// JavaScript function to create a Bootstrap navbar
function createNavbar() {
  // Create navbar element
  const navbar = document.createElement('nav');
  navbar.classList.add('navbar', 'navbar-expand-sm', 'navbar-dark','bg-dark', 'shadow-sm', 'pt-1', 'pb-1');

  // Create container for navbar content
  const container = document.createElement('div');
  container.classList.add('container');

  // Create logo in the center
  const logo = document.createElement('a');
  logo.classList.add('navbar-brand', 'mx-auto');

  // Create an image element for the logo
  const logoImage = document.createElement('img');
  logoImage.src = 'icons/biopin_logo2.png';
  logoImage.alt = 'Logo'; // Add alternative text for accessibility

  // Set the width and height attributes for resizing
  logoImage.width = 40;
  logoImage.height = 40;


  // Add the image to the logo
  logo.appendChild(logoImage);

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
