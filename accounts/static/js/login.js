const passwordField = document.getElementById('password');
const togglePassButton = document.getElementById('toggle-password');

// toggling password visibility
togglePassButton.addEventListener('click', function () {
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        togglePassButton.innerHTML = '<i class="fa-solid fa-eye-low-vision"></i';
    } else {
        passwordField.type = 'password';
        togglePassButton.innerHTML = '<i class="fa-solid fa-eye"></i>';
    }
});