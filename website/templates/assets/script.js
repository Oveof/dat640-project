function scrollToBottom() {
    const chatArea = document.querySelector('#chat-area');
    chatArea.scrollTop = chatArea.scrollHeight;
    document.querySelector('textarea[name="text"]').value = '';
}

function adjustChatAreaHeight() {
    const header = document.querySelector('header');
    const form = document.querySelector('#form');
    const chatArea = document.querySelector('#chat-area');
    const headerHeight = header.offsetHeight;
    const formHeight = form.offsetHeight;
    const availableHeight = window.innerHeight - headerHeight - formHeight;
    chatArea.style.maxHeight = availableHeight+"px";
}



document.getElementById('form').addEventListener('keydown', function(event) {
    console.log(event)
    if (event.ctrlKey && event.key === 'Enter') {
        event.preventDefault();  // Prevent default behavior
        this.querySelector('button[type="submit"]').click();  // Programmatically click the submit button
    }
});


window.addEventListener('load', adjustChatAreaHeight);
window.addEventListener('resize', adjustChatAreaHeight);