const passwordField = document.getElementById('password1')
const passToggleButton = document.getElementById('toggle-reg-password')

const conPasswordField = document.getElementById('password2')
const conPassToggleButton = document.getElementById('toggle-reg-con-password')


// toggling password visibility
passToggleButton.addEventListener('click', () => {
    if (passwordField.type === 'password') {
        passwordField.type = 'text'
        passToggleButton.innerHTML = '<i class="fa-solid fa-eye-low-vision"></i>'
    } else {
        passwordField.type = 'password'
        passToggleButton.innerHTML = '<i class="fa-solid fa-eye"></i>'
    }
})

conPassToggleButton.addEventListener('click', () => {
    if (conPasswordField.type === 'password') {
        conPasswordField.type = 'text'
        conPassToggleButton.innerHTML = '<i class="fa-solid fa-eye-low-vision"></i>'
    } else {
        conPasswordField.type = 'password'
        conPassToggleButton.innerHTML = '<i class="fa-solid fa-eye"></i>'
    }
})