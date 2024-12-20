custom_css = """
/* Main container styling */
.gradio-container {
    max-width: 1200px !important;
    margin: auto !important;
    padding: 20px !important;
}

/* Chat container styling */
.chat-container {
    height: 500px !important;
    overflow: hidden !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 8px !important;
    background: #ffffff !important;
}

/* Message styling */
.message {
    padding: 12px 16px !important;
    margin: 0 !important;
    border-bottom: 1px solid #e0e0e0 !important;
}

.message.user {
    background: #f9f9f9 !important;
}

.message.assistant {
    background: #ffffff !important;
}

/* Hide default avatars */
.avatar {
    display: none !important;
}

/* Message prefix styling */
.message.user::before {
    content: "User: " !important;
    font-weight: bold !important;
    color: #303030 !important;
}

.message.assistant::before {
    content: "AI Tools: " !important;
    font-weight: bold !important;
    color: #303030 !important;
}

/* Code container styling */
.code-container {
    height: 500px !important;
    overflow-y: auto !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 8px !important;
    background: #ffffff !important;
}

/* Input box styling */
.input-box {
    border: 1px solid #e0e0e0 !important;
}

footer {display: none !important}
""" 