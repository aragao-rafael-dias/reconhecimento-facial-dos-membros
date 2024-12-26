document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("uploadForm");
    const fileInput = document.getElementById("fileInput");
    const messageBox = document.getElementById("messageBox");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        if (!fileInput.files[0]) {
            displayMessage("Por favor, selecione uma foto!", "error");
            return;
        }

        const formData = new FormData(); // Corrigido o erro aqui
        formData.append("foto", fileInput.files[0]);

        try {
            const response = await fetch("/reconhecer", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                displayMessage(data.mensagem, "success"); // Corrigido "sucess" para "success"
            } else {
                displayMessage(data.mensagem, "error");
            }
        } catch (error) {
            console.error("Erro ao processar a solicitação:", error);
            displayMessage("Erro ao enviar a foto. Tente novamente!", "error");
        }
    });

    function displayMessage(message, type) {
        messageBox.textContent = message;
        messageBox.className = type; // Corrigido de message.className para messageBox.className
        messageBox.style.display = "block";

        setTimeout(() => {
            messageBox.style.display = "none";
        }, 5000);
    }
});
