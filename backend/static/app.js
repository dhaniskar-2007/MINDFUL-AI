document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const chatContainer = document.getElementById('chatContainer');
    const typingIndicator = document.getElementById('typingIndicator');
    const emotionBadge = document.getElementById('emotionBadge');

    let sessionId = sessionStorage.getItem('sessionId');
    if (!sessionId) {
        sessionId = crypto.randomUUID();
        sessionStorage.setItem('sessionId', sessionId);
    }

    const SVG_BOT = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>`;

    function addMessage(text, isUser = false, isCrisis = false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${isUser ? 'user-message' : 'system-message'}`;
        if (isCrisis) msgDiv.classList.add('crisis');

        let avatarHtml = isUser ? '' : `<div class="avatar">${SVG_BOT}</div>`;
        
        // Simple markdown parsing for bold and line breaks
        let formattedText = text.replace(/\n/g, '<br>');

        msgDiv.innerHTML = `
            ${avatarHtml}
            <div class="bubble">${formattedText}</div>
        `;
        
        chatContainer.appendChild(msgDiv);
        scrollToBottom();
    }

    function scrollToBottom() {
        chatContainer.scrollTo({
            top: chatContainer.scrollHeight,
            behavior: 'smooth'
        });
    }

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = messageInput.value.trim();
        if (!text) return;

        // Add user message to UI
        addMessage(text, true);
        messageInput.value = '';
        
        // Show typing indicator
        typingIndicator.style.display = 'block';
        scrollToBottom();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: text,
                    session_id: sessionId
                })
            });

            const data = await response.json();
            
            // Hide typing indicator
            typingIndicator.style.display = 'none';

            // Show emotion badge if not neutral
            if (data.detected_emotion !== 'Neutral') {
                emotionBadge.textContent = `Detected: ${data.detected_emotion}`;
                emotionBadge.style.display = 'block';
                // fade out badge after a bit
                setTimeout(() => { emotionBadge.style.display = 'none'; }, 4000);
            }

            // Append bot response
            addMessage(data.text, false, data.is_crisis);

        } catch (error) {
            console.error('Error:', error);
            typingIndicator.style.display = 'none';
            addMessage("I'm sorry, I'm having trouble connecting right now. Please try again in a moment.", false);
        }
    });

    // Optional: Auto-focus input
    messageInput.focus();
});
