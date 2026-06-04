document.addEventListener("DOMContentLoaded", () => {
    const chatHistory = document.getElementById("chat-history");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    function addMessage(text, isUser = false) {
        const msgDiv = document.createElement("div");
        msgDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
        
        const avatar = document.createElement("div");
        avatar.className = "avatar";
        avatar.innerHTML = isUser ? "👤" : "✨";
        
        const bubble = document.createElement("div");
        bubble.className = "bubble";
        
        // Simple formatting for line breaks
        bubble.innerHTML = text.replace(/\n/g, '<br>');
        
        msgDiv.appendChild(avatar);
        msgDiv.appendChild(bubble);
        chatHistory.appendChild(msgDiv);
        
        // Scroll to bottom
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function addTypingIndicator() {
        const msgDiv = document.createElement("div");
        msgDiv.className = "message ai-message typing-indicator-wrapper";
        msgDiv.id = "typing-indicator";
        
        const avatar = document.createElement("div");
        avatar.className = "avatar";
        avatar.innerHTML = "✨";
        
        const bubble = document.createElement("div");
        bubble.className = "bubble typing-indicator";
        bubble.innerHTML = "<span></span><span></span><span></span>";
        
        msgDiv.appendChild(avatar);
        msgDiv.appendChild(bubble);
        chatHistory.appendChild(msgDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function removeTypingIndicator() {
        const indicator = document.getElementById("typing-indicator");
        if (indicator) {
            indicator.remove();
        }
    }

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;
        
        // Add user message to UI
        addMessage(text, true);
        userInput.value = "";
        
        // Show typing indicator
        addTypingIndicator();
        
        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: text })
            });
            
            const data = await response.json();
            
            // Remove typing indicator and show AI response
            removeTypingIndicator();
            addMessage(data.response, false);
            
        } catch (error) {
            console.error("Error connecting to server:", error);
            removeTypingIndicator();
            addMessage("Sorry, I am having trouble connecting to the server. Please try again.", false);
        }
    }

    sendBtn.addEventListener("click", sendMessage);
    
    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            sendMessage();
        }
    });
});
