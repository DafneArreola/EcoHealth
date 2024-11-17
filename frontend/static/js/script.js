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
    });

    // Hide chatbot modal when the close button is clicked
    closeButton.addEventListener("click", function () {
        chatbotModal.style.display = "none";
    });

    // Handle sending messages and displaying responses
    sendMessageButton.addEventListener("click", async function () {
        const message = userInput.value.trim(); // Get user input
        if (message) {
            addMessageToChatlog("user", message); // Display user message
            userInput.value = ""; // Clear input field

            try {
                // Send user message to server and get chatbot response
                const response = await fetch("http://127.0.0.1:5000/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ message: message }),
                });

                const data = await response.json();
                addMessageToChatlog("bot", data.response); // Display chatbot response
            } catch (error) {
                addMessageToChatlog("bot", "Sorry, something went wrong. Please try again.");
                console.error("Error:", error);
            }
        }
    });

    // Function to add messages to the chatlog
    function addMessageToChatlog(role, message) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", role); // Add appropriate class for styling
        messageElement.textContent = message; // Set message text
        chatlog.appendChild(messageElement); // Append message to chatlog
        chatlog.scrollTop = chatlog.scrollHeight; // Auto-scroll to bottom
    }
});
