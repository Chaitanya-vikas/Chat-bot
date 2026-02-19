// Function to handle the chat logic
async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const message = inputField.value.trim();

    // If empty, do nothing
    if (message === "") return;

    // 1. Show YOUR message (Blue Bubble)
    appendMessage(message, "user-message");

    // Clear and focus input
    inputField.value = "";
    inputField.focus();

    // 2. Show TEMPORARY "Thinking..." bubble (Gray)
    // We save the ID so we can remove it later
    const loadingId = appendMessage("Thinking...", "bot-message");

    try {
        // 3. Send to Django Backend
        const response = await fetch('/ask/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        // 4. REMOVE the "Thinking..." bubble
        const loadingBubble = document.getElementById(loadingId);
        if (loadingBubble) {
            loadingBubble.remove();
        }

        // 5. ADD the Real Answer (Gray Bubble)
        // This ensures it is ALWAYS gray and fresh
        appendMessage(data.reply, "bot-message");

    } catch (error) {
        console.error("Error:", error);
        // If error, remove thinking and show error message
        const loadingBubble = document.getElementById(loadingId);
        if (loadingBubble) {
            loadingBubble.remove();
        }
        appendMessage("Sorry, my AI brain is offline.", "bot-message");
    }
}

// Helper to add bubbles to the chat
function appendMessage(text, className) {
    const chatBox = document.getElementById("chat-box");
    const msgDiv = document.createElement("div");

    // Create unique ID
    const id = "msg-" + Date.now() + Math.random(); 
    msgDiv.id = id;

    // Add Class (user-message = Blue, bot-message = Gray)
    msgDiv.classList.add("message", className);
    
    // Set Text
    msgDiv.innerText = text;

    // Add to Chat Box
    chatBox.appendChild(msgDiv);

    // Scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;

    return id; // Return ID so we can delete it later
}

// Allow "Enter" key to send
function handleEnter(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}