// Partículas Flotantes Naranjas en Fondo (Canvas)
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('bg-canvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let particles = [];

        function resize() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resize);
        resize();

        class Particle {
            constructor() {
                this.reset();
            }
            reset() {
                this.x = Math.random() * canvas.width;
                this.y = canvas.height + Math.random() * 50;
                this.size = Math.random() * 3.5 + 1;
                this.speedY = Math.random() * 1.2 + 0.4;
                this.speedX = (Math.random() - 0.5) * 0.6;
                this.opacity = Math.random() * 0.7 + 0.2;
            }
            update() {
                this.y -= this.speedY;
                this.x += this.speedX;
                if (this.y < -10) this.reset();
            }
            draw() {
                ctx.fillStyle = `rgba(212, 175, 55, ${this.opacity})`;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
            }
        }

        for (let i = 0; i < 50; i++) {
            particles.push(new Particle());
        }

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(p => {
                p.update();
                p.draw();
            });
            requestAnimationFrame(animate);
        }
        animate();
    }
});

// Control del Chatbot
function openChatModal() {
    const modal = document.getElementById('chat-modal');
    if (modal) modal.classList.add('active');
}

function closeChatModal() {
    const modal = document.getElementById('chat-modal');
    if (modal) modal.classList.remove('active');
}

document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');

    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = userInput.value.trim();
            if (!message) return;

            appendMessage('user-message', message, 'Tú');
            userInput.value = '';

            // Mostrar estado "pensando..."
            const loadingId = appendLoadingMessage();

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();
                removeLoadingMessage(loadingId);
                appendMessage('bot-message', data.response, 'Mini Tinto');
            } catch (error) {
                removeLoadingMessage(loadingId);
                appendMessage('bot-message', '¡Uy parce! Tuve un problemita al conectar. ¡Intenta de nuevo!', 'Mini Tinto');
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
            <div>${text}</div>
        `;
    } else {
        msgDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
    }

    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function appendLoadingMessage() {
    const chatBox = document.getElementById('chat-box');
    const msgDiv = document.createElement('div');
    const id = 'loading-' + Date.now();
    msgDiv.id = id;
    msgDiv.classList.add('message', 'bot-message');
    msgDiv.innerHTML = `
        <div class="bot-info-user">
            <img src="/img/mini-tinto.jpg" class="mini-icon" alt="Mini Tinto">
            <strong>Mini Tinto:</strong>
        </div>
        <em>☕ Pensando y preparando la respuesta...</em>
    `;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    return id;
}

function removeLoadingMessage(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}
