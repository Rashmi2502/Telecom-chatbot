document.addEventListener("DOMContentLoaded", function() {
    // Get elements
    const welcomeScreen = document.getElementById("welcome-screen");
    const startChatButton = document.getElementById("start-chat-btn");
    const chatScreen = document.getElementById("chat-screen");
    const sendButton = document.getElementById("send-btn");
    const userInput = document.getElementById("user-input");
    const chatHistory = document.getElementById("chat-history");

    // Show the chat screen when "Start Chat" button is clicked
    startChatButton.addEventListener("click", function() {
        welcomeScreen.style.display = "none";
        chatScreen.style.display = "block";
    });

    // Send a message to the bot when the "Send" button is clicked or enter is pressed
    sendButton.addEventListener("click", function() {
        sendMessage();
    });

    // Handle enter key press for sending messages
    userInput.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    // Function to send message and interact with the chatbot
    function sendMessage() {
        const message = userInput.value.trim();
        if (message) {
            // Append user message to chat history
            const userMessageDiv = document.createElement("div");
            userMessageDiv.classList.add("user-message");
            userMessageDiv.textContent = `You: ${message}`;  // Correct string interpolation
            chatHistory.appendChild(userMessageDiv);

            // Clear input field
            userInput.value = "";

            // Call the chatbot API
            fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            })
            .then(response => response.json())
            .then(data => {
                // Append chatbot response to chat history
                const botMessageDiv = document.createElement("div");
                botMessageDiv.classList.add("bot-message");
                botMessageDiv.textContent = `Bot: ${data.reply}`;  // Correct string interpolation
                chatHistory.appendChild(botMessageDiv);

                // Scroll to the bottom of the chat
                chatHistory.scrollTop = chatHistory.scrollHeight;
            })
            .catch(error => {
                const errorMessageDiv = document.createElement("div");
                errorMessageDiv.classList.add("error-message");
                errorMessageDiv.textContent = "Error: Unable to get a response from the chatbot.";
                chatHistory.appendChild(errorMessageDiv);
            });
        }
    }
});
