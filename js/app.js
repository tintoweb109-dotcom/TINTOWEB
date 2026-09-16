document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message) return;

        // Renderizar mensaje del usuario
        appendMessage(message, "user-message");
        userInput.value = "";

        // Renderizar indicador de carga
        const loadingDiv = appendMessage("Pensando la respuesta, parcero...", "bot-message");

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();

            if (response.ok) {
                loadingDiv.textContent = data.response;
            } else {
                loadingDiv.textContent = "Uy compa, ocurrió un error: " + (data.error || "Error desconocido");
            }
        } catch (error) {
            loadingDiv.textContent = "Parce, no me pude conectar con el servidor. Revisa tu conexión a internet.";
        }

        scrollToBottom();
    });

    function appendMessage(text, className) {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message", className);
        msgDiv.textContent = text;
        chatBox.appendChild(msgDiv);
        scrollToBottom();
        return msgDiv;
    }

    function scrollToBottom() {
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
