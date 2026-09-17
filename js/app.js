document.addEventListener("DOMContentLoaded", () => {
    // 1. Partículas Canvas de Fondo
    initCanvasBackground();

    // 2. Animaciones GSAP de Entrada al Scroll
    if (typeof gsap !== "undefined" && typeof ScrollTrigger !== "undefined") {
        gsap.registerPlugin(ScrollTrigger);

        gsap.utils.toArray(".reveal-card").forEach((card) => {
            gsap.from(card, {
                scrollTrigger: {
                    trigger: card,
                    start: "top 85%",
                },
                opacity: 0,
                y: 40,
                duration: 0.7,
                ease: "power2.out"
            });
        });

        gsap.from(".hero-content", {
            opacity: 0,
            y: -30,
            duration: 0.9,
            ease: "power3.out"
        });
    }

    // 3. Manejo interactivo del Chatbot
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const tintoAvatars = document.querySelectorAll(".mini-tinto-alive");

    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const message = userInput.value.trim();
        if (!message) return;

        appendMessage("user", message);
        userInput.value = "";

        // Activar animación de hablar a Mini Tinto
        tintoAvatars.forEach(img => img.classList.add("tinto-talking"));

        const loadingDiv = document.createElement("div");
        loadingDiv.classList.add("message", "bot-message");
        loadingDiv.id = "loading-indicator";
        loadingDiv.innerHTML = `
            <div class="bot-info-user">
                <img src="/img/mini-tinto.jpg" class="mini-icon mini-tinto-alive" alt="Mini Tinto">
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

            // Desactivar animación de hablar
            tintoAvatars.forEach(img => img.classList.remove("tinto-talking"));

            if (response.ok && data.response) {
                appendMessage("bot", data.response);
            } else {
                appendMessage("bot", "¡Uy parcero! Tuve un problema al procesar la respuesta. Inténtalo de nuevo.");
            }
        } catch (error) {
            tintoAvatars.forEach(img => img.classList.remove("tinto-talking"));
            const indicator = document.getElementById("loading-indicator");
            if (indicator) indicator.remove();
            appendMessage("bot", "Error de conexión con el servidor. Revisa tu red o intenta más tarde.");
        }
    });

    function appendMessage(sender, text) {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");

        if (sender === "bot") {
            msgDiv.innerHTML = `
                <div class="bot-info-user">
                    <img src="/img/mini-tinto.jpg" class="mini-icon mini-tinto-alive" alt="Mini Tinto">
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

// Canvas de Partículas Interactivas de Fondo
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

    const particles = Array.from({ length: 40 }, () => ({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * 2 + 1,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4,
        alpha: Math.random() * 0.5 + 0.2
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

function scrollToChat() {
    const chatSection = document.getElementById("chat-section");
    if (chatSection) {
        chatSection.scrollIntoView({ behavior: "smooth" });
        setTimeout(() => {
            document.getElementById("user-input").focus();
        }, 600);
    }
}
