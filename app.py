// Abrir y cerrar el modal del chat
function openChatModal() {
    const modal = document.getElementById('chat-modal');
    if (modal) {
        modal.classList.add('active');
    }
}

function closeChatModal() {
    const modal = document.getElementById('chat-modal');
    if (modal) {
        modal.classList.remove('active');
    }
}

// Envío de mensajes al servidor Flask
document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');

    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = userInput.value.trim();
            if (!message) return;

            // Agregar mensaje del usuario a la pantalla
            appendMessage('user-message', message, 'Tú');
            userInput.value = '';

            try {
                // Petición al backend Flask
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();
                appendMessage('bot-message', data.response, 'Mini Tinto');
            } catch (error) {
                appendMessage('bot-message', '¡Uy parce! Ocurrió un error al conectar con el servidor. Intenta de nuevo.', 'Mini Tinto');
            }
        });
    }
});

function appendMessage(className, text, sender) {
    const chatBox = document.getElementById('chat-box');
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', className);
    
    if (className === 'bot-message') {
        msgDiv.innerHTML = `
            <div class="bot-info-user">
                <img src="/img/mini-tinto.jpg" class="mini-icon" alt="Mini Tinto">
                <strong>${sender}:</strong>
            </div>
            ${text}
        `;
    } else {
        msgDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
    }

    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
