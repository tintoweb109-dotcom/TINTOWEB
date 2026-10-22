document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');

    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = userInput.value.trim();
            if (!message) return;

            // Agregar mensaje del usuario a la pantalla
            appendMessage('Tú', message, 'user-message', false);
            userInput.value = '';

            try {
                // Enviar mensaje al backend en Flask
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();
                
                // Agregar respuesta de Mini Tinto a la pantalla
                appendMessage('Mini Tinto', data.response, 'bot-message', true);

            } catch (error) {
                console.error('Error al conectar con el servidor:', error);
                appendMessage('Mini Tinto', 'Mil disculpas, señor. Ocurrió un error temporal de conexión. ☕', 'bot-message', true);
            }
        });
    }
});

// Función para formatear el texto (convierte **títulos** en negritas resaltadas)
function formatMessage(text) {
    if (!text) return '';
    return text.replace(/\*\*(.*?)\*\*/g, '<strong style="color: #f59e0b; display: block; margin-top: 6px;">$1</strong>');
}

// Función para renderizar los mensajes en el contenedor del chat
function appendMessage(sender, text, className, isBot) {
    const chatBox = document.getElementById('chat-box');
    if (!chatBox) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${className}`;

    if (isBot) {
        messageDiv.innerHTML = `
            <div class="bot-info-user" style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                <img src="/img/mini-tinto.jpg" class="mini-icon" alt="Mini Tinto" style="width: 26px; height: 26px; border-radius: 50%;">
                <strong style="color: #38bdf8;">${sender}:</strong>
            </div>
            <div style="white-space: pre-wrap; line-height: 1.6; padding-left: 34px;">${formatMessage(text)}</div>
        `;
    } else {
        messageDiv.innerHTML = `
            <strong style="color: #e2e8f0;">${sender}:</strong> 
            <span style="white-space: pre-wrap; line-height: 1.5; color: #cbd5e1;">${text}</span>
        `;
    }

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
