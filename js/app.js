document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const message = userInput.value.trim();
        if (!message) return;

        // 1. Mostrar mensaje del usuario
        appendMessage("user", message);
        userInput.value = "";

        // 2. Mostrar indicador de cargando
        const loadingDiv = document.createElement("div");
        loadingDiv.classList.add("message", "bot-message");
        loadingDiv.id = "loading-indicator";
        loadingDiv.innerHTML = `
            <div class="bot-info-user">
                <img src="/img/mini-tinto.png" class="mini-icon" alt="Mini Tinto">
                <strong>Mini Tinto:</strong>
            </div>
            <em>Escribiendo... ☕</em>
        `;
        chatBox.appendChild(loadingDiv);
        chatBox.scrollTop = chatBox.scrollHeight;

        try {
            // 3. Petición al servidor Backend Flask
            const response = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            
            // Remover indicador de carga
            const indicator = document.getElementById("loading-indicator");
            if (indicator) indicator.remove();

            if (response.ok && data.response) {
                appendMessage("bot", data.response);
            } else {
                appendMessage("bot", "¡Uy parcero! Tuve un inconveniente técnico al responder. Inténtalo de nuevo en un segundo.");
            }
        } catch (error) {
            console.error("Error en la solicitud:", error);
            const indicator = document.getElementById("loading-indicator");
            if (indicator) indicator.remove();
            appendMessage("bot", "Parece que hay un problema de conexión con el servidor. Revisa tu red o intenta más tarde.");
        }
    });

    function appendMessage(sender, text) {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");

        if (sender === "bot") {
            msgDiv.innerHTML = `
                <div class="bot-info-user">
                    <img src="/img/mini-tinto.png" class="mini-icon" alt="Mini Tinto">
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

// Función suave para desplazarse al chat
function scrollToChat() {
    const chatSection = document.getElementById("chat-section");
    if (chatSection) {
        chatSection.scrollIntoView({ behavior: "smooth" });
        setTimeout(() => {
            document.getElementById("user-input").focus();
        }, 600);
    }
}
