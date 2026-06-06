const form = document.getElementById("chatForm");
const input = document.getElementById("question");
const messages = document.getElementById("messages");

let chatHistory = [];

document.querySelectorAll(".suggestions button").forEach(button => {

    button.addEventListener("click", () => {

        input.value = button.innerText;
        input.focus();

    });

});

function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {

        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {

            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {

                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );

                break;
            }
        }
    }

    return cookieValue;
}

function addMessage(text, type) {

    const message = document.createElement("div");

    message.className =
        type === "user"
            ? "user-message"
            : "bot-message";

    message.innerHTML = text;

    messages.appendChild(message);

    messages.scrollTop = messages.scrollHeight;

    return message;
}

form.addEventListener("submit", async function (e) {

    e.preventDefault();

    const question = input.value.trim();

    if (!question) return;

    addMessage(question, "user");

    input.value = "";

    const botMessage = addMessage(
        "🌾 Thinking...",
        "bot"
    );

    try {

        const response = await fetch(
            "/chatbot/",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },

                body: JSON.stringify({
                    question: question,
                    history: chatHistory
                })
            }
        );

        const data = await response.json();

        botMessage.innerHTML = data.answer;

        chatHistory.push({
            question: question,
            answer: data.answer
        });

        messages.scrollTop = messages.scrollHeight;

    }
    catch (error) {

        console.error(error);

        botMessage.innerHTML =
            "❌ Unable to get response from server.";

    }

});