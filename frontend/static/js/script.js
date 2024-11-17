document.addEventListener("DOMContentLoaded", function () {
    const chatbotButton = document.getElementById("chatbot-button");
    const chatbotModal = document.getElementById("chatbot-modal");
    const closeButton = document.getElementById("close-chatbot");
    const sendMessageButton = document.getElementById("send-message");
    const userInput = document.getElementById("user-input");
    const chatlog = document.getElementById("chatlog");
    const suggestionsContainer = document.getElementById("chat-suggestions");

    // Show chatbot modal when the button is clicked
    chatbotButton.addEventListener("click", function () {
        chatbotModal.style.display = "block";
        // Add welcome message when chat is opened
        if (chatlog.children.length === 0) {
            addMessageToChatlog("bot", "Hi! I'm here to help you on your eco-health journey. What's on your mind?");
            showSuggestions();
        }
    });

    function showSuggestions() {
        const suggestions = [
            "Lacking motivation? 🌱",
            "Want to make a difference? 🌍",
            "Feeling overwhelmed? 💭"
        ];

        suggestionsContainer.innerHTML = '';
        suggestions.forEach(suggestion => {
            const button = document.createElement('button');
            button.className = 'suggestion-button';
            button.textContent = suggestion;
            button.onclick = function() {
                userInput.value = suggestion;
                sendMessage();
                suggestionsContainer.style.display = 'none';
            };
            suggestionsContainer.appendChild(button);
        });
        suggestionsContainer.style.display = 'flex';
    }

    // Hide chatbot modal when the close button is clicked
    closeButton.addEventListener("click", function () {
        chatbotModal.style.display = "none";
    });

    // Handle sending messages when Enter key is pressed
    userInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    // Handle sending messages and displaying responses
    sendMessageButton.addEventListener("click", sendMessage);

    async function sendMessage() {
        const message = userInput.value.trim();
        if (message) {
            addMessageToChatlog("user", message);
            userInput.value = "";
            suggestionsContainer.style.display = 'none';

            try {
                const response = await fetch("/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ message: message }),
                });

                const data = await response.json();
                if (data.status === 'success') {
                    addMessageToChatlog("bot", data.response);
                } else {
                    throw new Error(data.response || 'Failed to get response');
                }
            } catch (error) {
                console.error("Error:", error);
                addMessageToChatlog("bot", "Sorry, something went wrong. Please try again.");
            }
        }
    }

    function addMessageToChatlog(role, message) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", role);
        messageElement.innerHTML = `
            <div class="message-content">
                <span class="message-icon">${role === "user" ? "👤" : "🤖"}</span>
                <span class="message-text">${message}</span>
            </div>
        `;
        chatlog.appendChild(messageElement);
        chatlog.scrollTop = chatlog.scrollHeight;
    }

    // Show suggestions when input is empty
    userInput.addEventListener('input', function() {
        if (!userInput.value.trim()) {
            showSuggestions();
        } else {
            suggestionsContainer.style.display = 'none';
        }
    });
});