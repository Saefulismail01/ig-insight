// Chat Widget
const Chat = {
    init() {
        // Create chat widget HTML
        const chatHTML = `
            <div id="chatToggleBtn" class="chat-floating-button">💬</div>
            <div id="chatWidget" class="chat-widget collapsed">
                <div class="chat-widget-header">
                    <div class="chat-header-info">
                        <h4>AI Data Analyst</h4>
                        <p>Ask anything about your data</p>
                    </div>
                    <button id="chatCloseBtn">✕</button>
                </div>
                <div class="chat-container">
                    <div id="chatMessages" class="chat-messages">
                        <div class="message ai-message">
                            <div class="message-header">
                                <span class="message-icon">🤖</span>
                                <span class="message-author">AI Analyst</span>
                            </div>
                            <div class="message-content">
                                Hello! I'm your AI data analyst. I can help you analyze your Instagram data, identify trends, and provide recommendations. Feel free to ask me anything!
                            </div>
                        </div>
                    </div>
                    <div class="chat-input-container">
                        <input type="text" id="chatInput" placeholder="Ask about your data..." class="chat-input">
                        <button id="chatSendBtn" class="chat-send-btn">
                            <span>Send</span>
                            <span>→</span>
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', chatHTML);

        // Add event listeners
        document.getElementById('chatToggleBtn').addEventListener('click', () => this.toggle());
        document.getElementById('chatCloseBtn').addEventListener('click', () => this.toggle(false));
        document.getElementById('chatSendBtn').addEventListener('click', () => this.sendMessage());
        document.getElementById('chatInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    },

    toggle(open) {
        const widget = document.getElementById('chatWidget');
        const btn = document.getElementById('chatToggleBtn');
        
        if (open === undefined) {
            open = widget.classList.contains('collapsed');
        }

        if (open) {
            widget.classList.remove('collapsed');
            btn.classList.add('active');
        } else {
            widget.classList.add('collapsed');
            btn.classList.remove('active');
        }
    },

    async sendMessage() {
        const input = document.getElementById('chatInput');
        const message = input.value.trim();
        
        if (!message) return;

        const chatMessages = document.getElementById('chatMessages');
        
        // Add user message
        this.addMessage('user', message);
        input.value = '';

        // Show typing indicator
        const typingDiv = this.addTypingIndicator();
        
        try {
            const history = this.getHistory();
            const response = await API.sendChatMessage(message, history);
            
            // Remove typing indicator
            typingDiv.remove();
            
            // Add AI response
            if (response.error) {
                this.addMessage('error', response.error);
            } else {
                this.addMessage('ai', response.response || 'Sorry, I couldn\'t generate a response.');
            }
        } catch (error) {
            typingDiv.remove();
            this.addMessage('error', 'Sorry, I encountered an error. Please try again.');
        }

        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    },

    addMessage(type, content) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        
        const isUser = type === 'user';
        const isError = type === 'error';
        const icon = isUser ? '👤' : (isError ? '⚠️' : '🤖');
        const author = isUser ? 'You' : (isError ? 'Error' : 'AI Analyst');
        
        messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
        messageDiv.innerHTML = `
            <div class="message-header">
                <span class="message-icon">${icon}</span>
                <span class="message-author">${author}</span>
            </div>
            <div class="message-content">${content}</div>
        `;
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    },

    addTypingIndicator() {
        const chatMessages = document.getElementById('chatMessages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message ai-message';
        typingDiv.innerHTML = `
            <div class="message-header">
                <span class="message-icon">🤖</span>
                <span class="message-author">AI Analyst</span>
            </div>
            <div>
                <span class="typing-indicator"></span>
                <span class="typing-indicator"></span>
                <span class="typing-indicator"></span>
            </div>
        `;
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return typingDiv;
    },

    getHistory() {
        const messages = document.querySelectorAll('#chatMessages .message');
        const history = [];
        
        messages.forEach(msg => {
            const isAI = msg.classList.contains('ai-message');
            const content = msg.querySelector('.message-content');
            if (content && !msg.querySelector('.typing-indicator')) {
                history.push({
                    role: isAI ? 'assistant' : 'user',
                    content: content.textContent.trim()
                });
            }
        });
        
        return history.slice(-10);
    }
};
