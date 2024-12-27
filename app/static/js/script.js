document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("uploadForm");
    const fileInput = document.getElementById("fileInput");
    const messageBox = document.getElementById("messageBox");
    const listaPresencas = document.getElementById("listaPresenca");
    const btnEnviarPDF = document.getElementById("btnEnviarPDF");
    const btnEnviarFoto = document.getElementById("btnEnviarFoto");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        btnEnviarFoto.disabled = true;
        btnEnviarPDF.disabled = true;

        if (!fileInput.files[0]) {
            displayMessage("Por favor, selecione uma foto!", "error");
            btnEnviarFoto.disabled = false;
            btnEnviarPDF.disabled = false;
            return;
        }

        const formData = new FormData(); 
        formData.append("foto", fileInput.files[0]);

        try {
            const response = await fetch("/reconhecer", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                displayMessage(data.mensagem, "success"); 
            } else {
                displayMessage(data.mensagem, "error");
            }
        } catch (error) {
            console.error("Erro ao processar a solicitação:", error);
            displayMessage("Erro ao enviar a foto. Tente novamente!", "error");
        } finally {
            btnEnviarFoto.disabled = false;
            btnEnviarPDF = false;
        }
    });

    async function atualizarLista() {
        try {
            const response = await fetch("/lista_presencas");
            const data = await response.json();

            listaPresencas.innerHTML = "";

            data.presentes.forEach((presenca) => {
                const item = document.createElement("li");
                item.textContent = `${presenca.nome} - ${presenca.hora}`;
                listaPresencas.appendChild(item);
            });
        } catch (error) {
            console.error("Erro ao atualizar a lista de presenças:", error)
        }
    }

    btnEnviarPDF.addEventListener("click", async () => {
        try {
            const response = await fetch("/gerar_pdf", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();
            displayMessage(data.mensagem, response.ok ? "success" : "error");
        } catch (error) {
            console.error("Erro ao enviar o PDF", error);
            displayMessage("Erro ao enviar o PDF. Tente novamente!", "error");
        }
    });

    function displayMessage(message, type) {
        messageBox.textContent = message;
        messageBox.className = type; 
        messageBox.style.display = "block";

        setTimeout(() => {
           messageBox.style.display = "none";
        }, 5000);
    }
});
