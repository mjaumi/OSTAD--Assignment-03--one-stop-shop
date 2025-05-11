const messageContainer = document.getElementById('message-container');
const messageButton = document.getElementById('message-button');

// hiding message container
messageButton.addEventListener('click', function () {
    messageContainer.classList.add('hidden');
});