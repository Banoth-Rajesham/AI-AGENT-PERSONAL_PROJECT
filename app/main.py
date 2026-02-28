from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from app.core.agent import Agent
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
agent = Agent()


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(request: ChatRequest):
    response = agent.run(request.message)
    return {"response": response}
    


@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>AI Agent</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="/static/styles.css?v=12345">
</head>
<body>

<header>
    <div class="title">AI Agent</div>
</header>

<div id="chat-container">
    <div id="chat-inner"></div>
</div>

<div id="input-bar">
    <div id="input-bar-inner">
        <input id="message-input" placeholder="Ask something..." autocomplete="off" />
        <button id="send-btn">Send</button>
    </div>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {

    const input = document.getElementById("message-input");
    const chatContainer = document.getElementById("chat-container");
    const chat = document.getElementById("chat-inner");
    const sendBtn = document.getElementById("send-btn");

    input.focus();

    function scrollToBottom(force = false) {

        const isNearBottom =
            chatContainer.scrollHeight -
            chatContainer.scrollTop -
            chatContainer.clientHeight < 120;

        if (force || isNearBottom) {
            chatContainer.scrollTo({
                top: chatContainer.scrollHeight,
                behavior: "smooth"
            });
        }
    }

    function addMessage(text, type) {

        const wrapper = document.createElement("div");
        wrapper.className = "message " + type;

        const inner = document.createElement("div");
        inner.className = "message-inner";
        inner.textContent = text;

        wrapper.appendChild(inner);

        if (type === "agent") {
            const actions = document.createElement("div");
            actions.className = "message-actions";
            actions.innerHTML = "👍 👎 🔄 📋";
            wrapper.appendChild(actions);
        }

        chat.appendChild(wrapper);
        scrollToBottom(true);
    }

    function addTyping() {

        const typing = document.createElement("div");
        typing.className = "message agent";
        typing.id = "typing";

        const inner = document.createElement("div");
        inner.className = "message-inner";
        inner.textContent = "Thinking...";

        typing.appendChild(inner);
        chat.appendChild(typing);

        scrollToBottom(true);
    }

    function removeTyping() {
        const typing = document.getElementById("typing");
        if (typing) typing.remove();
    }

    async function sendMessage() {

        const text = input.value.trim();
        if (!text) return;

        sendBtn.disabled = true;

        addMessage(text, "user");
        input.value = "";
        addTyping();

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();

            removeTyping();
            addMessage(data.response || "No response", "agent");

        } catch (error) {
            removeTyping();
            addMessage("Server error", "agent");
        }

        sendBtn.disabled = false;
        input.focus();
    }

    sendBtn.addEventListener("click", sendMessage);

    input.addEventListener("keydown", function(e) {
        if (e.key === "Enter" && !sendBtn.disabled) {
            e.preventDefault();
            sendMessage();
        }
    });

});
</script>

</body>
</html>
"""