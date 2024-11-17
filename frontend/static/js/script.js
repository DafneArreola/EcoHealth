document.addEventListener("DOMContentLoaded", function () {
    const chatbotButton = document.getElementById("chatbot-button");
    const chatbotModal = document.getElementById("chatbot-modal");
    const closeButton = document.getElementById("close-chatbot");
    const sendMessageButton = document.getElementById("send-message");
    const userInput = document.getElementById("user-input");
    const chatlog = document.getElementById("chatlog");

    // Show chatbot modal when the button is clicked
    chatbotButton.addEventListener("click", function () {
        chatbotModal.style.display = "block";
        // Add welcome message when chat is opened
        if (chatlog.children.length === 0) {
            addMessageToChatlog("bot", "Hi! I'm here to help you on your eco-health journey. What's on your mind?");
        }
    });

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

    // Handle sending messages when Send button is clicked
    sendMessageButton.addEventListener("click", sendMessage);

    async function sendMessage() {
        const message = userInput.value.trim();
        if (message) {
            addMessageToChatlog("user", message);
            userInput.value = "";

            try {
                // Get CSRF token from meta tag
                const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
                
                // Send message to server
                const response = await fetch("/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrfToken || "",
                    },
                    body: JSON.stringify({ message: message }),
                    credentials: 'same-origin'
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                
                if (data.status === "success") {
                    addMessageToChatlog("bot", data.response);
                } else {
                    throw new Error(data.response || "Failed to get response");
                }
            } catch (error) {
                console.error("Chat error:", error);
                addMessageToChatlog("bot", "Sorry, I'm having trouble responding right now. Please try again in a moment.");
            }
        }
    }

    function addMessageToChatlog(role, message) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", role);
        
        // Create message content wrapper
        const contentWrapper = document.createElement("div");
        contentWrapper.classList.add("message-content");
        
        // Add icon/avatar element
        const iconElement = document.createElement("span");
        iconElement.classList.add("message-icon");
        iconElement.textContent = role === "user" ? "👤" : "🤖";
        
        // Add text content
        const textElement = document.createElement("span");
        textElement.classList.add("message-text");
        textElement.textContent = message;
        
        // Assemble message
        contentWrapper.appendChild(iconElement);
        contentWrapper.appendChild(textElement);
        messageElement.appendChild(contentWrapper);
        
        chatlog.appendChild(messageElement);
        chatlog.scrollTop = chatlog.scrollHeight;
    }
});