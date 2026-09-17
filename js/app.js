document.addEventListener("DOMContentLoaded", () => {
    initCanvasBackground();

    // Animaciones GSAP suaves
    if (typeof gsap !== "undefined" && typeof ScrollTrigger !== "undefined") {
        gsap.registerPlugin(ScrollTrigger);

        gsap.utils.toArray(".card, .creator-card, .cta-card").forEach((card) => {
            gsap.from(card, {
                scrollTrigger: {
                    trigger: card,
                    start: "top 85%",
                },
                opacity: 0,
                y: 35,
                duration: 0.6,
                ease: "power2.out"
            });
        });

        gsap.from(".hero-content", {
            opacity: 0,
            y: -25,
            duration: 0.8,
            ease: "power3.out"
        });
    }

    // Peticiones AJAX al servidor Flask (/chat)
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    if (chatForm) {
        chatForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const message = userInput.value.trim();
            if (!message) return;

            appendMessage("user", message);
            userInput.value = "";

            // Indicador de "Escribiendo..."
            const loadingDiv = document.createElement("div");
            loadingDiv.classList.add("message", "bot-message");
            loadingDiv.id = "loading-indicator";
            loadingDiv.innerHTML = `
                <div class="bot-info-user">
                    <img src="/static/img/mini-tinto.jpg" class="mini-icon" alt="Mini Tinto">
                    <strong>Mini Tinto:</strong>
                </div>
                <em>Escribiendo... ☕</em>
            `;
            chatBox.appendChild(loadingDiv);
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const response = await fetch("/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();
                const indicator = document.getElementById("loading-indicator");
                if (indicator) indicator.remove();

                if (response.ok && data.response) {
                    appendMessage("bot", data.response);
                } else {
                    appendMessage("bot", "¡Uy parcero! Tuve un problema al procesar la respuesta. Inténtalo de nuevo.");
                }
            } catch (error) {
                const indicator = document.getElementById("loading-indicator");
                if (indicator) indicator.remove();
                appendMessage("bot", "Error de conexión con el servidor. Revisa tu red o intenta más tarde.");
            }
        });
    }

    function appendMessage(sender, text) {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");

        if (sender === "bot") {
            msgDiv.innerHTML = `
                <div class="bot-info-user">
                    <img src="/static/img/mini-tinto.jpg" class="mini-icon" alt="Mini Tinto">
                    <strong>Mini Tinto:</strong>
                </div>
                ${text.replace(/\n/g, "<br>")}
            `;
        } else {
            msgDiv.textContent = text;
        }

        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});

// Modal de Chat
function openChatModal() {
    const modal = document.getElementById("chat-modal");
    if (modal) {
        modal.classList.add("active");
        setTimeout(() => {
            const input = document.getElementById("user-input");
            if (input) input.focus();
        }, 200);
    }
}

function closeChatModal() {
    const modal = document.getElementById("chat-modal");
    if (modal) {
        modal.classList.remove("active");
    }
}

// Fondo de Partículas Interactivas
function initCanvasBackground() {
    const canvas = document.getElementById("bg-canvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    window.addEventListener("resize", () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    });

    const particles = Array.from({ length: 35 }, () => ({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * 2 + 1,
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3,
        alpha: Math.random() * 0.4 + 0.1
    }));

    function animate() {
        ctx.clearRect(0, 0, width, height);
        particles.forEach((p) => {
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0) p.x = width;
            if (p.x > width) p.x = 0;
            if (p.y < 0) p.y = height;
            if (p.y > height) p.y = 0;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(245, 158, 11, ${p.alpha})`;
            ctx.fill();
        });
        requestAnimationFrame(animate);
    }
    animate();
}
