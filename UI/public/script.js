document.addEventListener('DOMContentLoaded', function () {
    // Load JSON data
    fetch('bluetooth.json')
      .then(response => response.json())
      .then(data => {
        // Check the value of the headgearStatus variable
        if (data.headgearStatus === 1) {
          // Update toast content if connected
          document.getElementById('headgearToast').querySelector('.toast-body').textContent = 'Headgear connected.';
        }
  
        // Show the toast
        new bootstrap.Toast(document.getElementById('headgearToast')).show();
      })
      .catch(error => console.error('Error loading JSON:', error));
  });
  