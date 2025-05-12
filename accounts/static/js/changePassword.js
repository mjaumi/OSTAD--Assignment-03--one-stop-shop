const oldPassField = document.getElementById('old_password');
const newPassField = document.getElementById('new_password1');
const confirmPassField = document.getElementById('new_password2');

const toggleOldBtn = document.getElementById('toggle-old-password');
const toggleNewBtn = document.getElementById('toggle-new-password');
const toggleConfirmBtn = document.getElementById('toggle-con-password');

toggleOldBtn.addEventListener('click', () => {
    if (oldPassField.type === 'password') {
        oldPassField.type = 'text';
        togglePassButton.innerHTML = '<i class="fa-solid fa-eye-low-vision"></i';
    } else {
        oldPassField.type = 'password';
        togglePassButton.innerHTML = '<i class="fa-solid fa-eye"></i>';
    }
});

toggleNewBtn.addEventListener('click', () => {
    if (newPassField.type === 'password') {
        newPassField.type = 'text';
        togglePassButton.innerHTML = '<i class="fa-solid fa-eye-low-vision"></i';
    } else {
        newPassField.type = 'password';
        togglePassButton.innerHTML = '<i class="fa-solid fa-eye"></i>';
    }
});

toggleConfirmBtn.addEventListener('click', () => {
    if (confirmPassField.type === 'password') {
        confirmPassField.type = 'text';
        togglePassButton.innerHTML = '<i class="fa-solid fa-eye-low-vision"></i';
    } else {
        confirmPassField.type = 'password';
        togglePassButton.innerHTML = '<i class="fa-solid fa-eye"></i>';
    }
});