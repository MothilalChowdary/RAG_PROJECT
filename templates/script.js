const API_BASE = "http://127.0.0.1:8000";
let chatHistory = JSON.parse(sessionStorage.getItem("chat_history")) || [];

// Initial Load & Auth UI
window.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById("chatContainer");
    const loginLink = document.getElementById("loginLink");
    const token = sessionStorage.getItem("access_token");

    if (chatHistory.length && chatContainer) {
        chatContainer.innerHTML = '';
        chatHistory.forEach(msg => appendMessage(msg.role, msg.content, msg.sources, false));
    }

    if (token && loginLink) {
        loginLink.innerText = "Logout";
        loginLink.onclick = () => { sessionStorage.clear(); window.location.reload(); };
    }
});

function appendMessage(role, text, sources = [], save = true) {
    const chatContainer = document.getElementById("chatContainer");
    if (!chatContainer) return;

    const div = document.createElement("div");
    div.className = `chat-bubble ${role}`;
    div.innerHTML = `<div>${text}</div>` +
        (sources?.length ? `<div class="sources">${sources.map(s => `<span class="source-tag">${s}</span>`).join('')}</div>` : '');

    chatContainer.appendChild(div);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    if (save) {
        chatHistory.push({ role, content: text, sources });
        sessionStorage.setItem("chat_history", JSON.stringify(chatHistory));
    }
}

async function handleSubmission() {
    const input = document.getElementById("query");
    const query = input.value.trim();
    if (!query) return;

    appendMessage("user", query);
    input.value = "";

    try {
        const token = sessionStorage.getItem("access_token");
        const res = await fetch(`${API_BASE}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...(token && { "Authorization": `Bearer ${token}` })
            },
            body: JSON.stringify({ query, chat_history: chatHistory.map(({ role, content }) => ({ role, content })) })
        });

        const data = await res.json();
        if (res.ok) appendMessage("assistant", data.response[0], data.response[1]);
        else if (res.status === 401) { alert("Session expired"); window.location.href = "login.html"; }
    } catch (e) { console.error(e); }
}

// Event Listeners
document.getElementById("askBtn")?.addEventListener("click", handleSubmission);
document.getElementById("query")?.addEventListener("keydown", e => e.key === "Enter" && handleSubmission());
document.getElementById("clearBtn")?.addEventListener("click", () => { sessionStorage.removeItem("chat_history"); window.location.reload(); });

// Login logic
document.getElementById("loginForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const res = await fetch(`${API_BASE}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({ username, password })
        });
        const data = await res.json();
        if (res.ok) {
            sessionStorage.setItem("access_token", data.access_token);
            window.location.href = "input.html";
        } else alert(data.detail || "Login failed");
    } catch (err) { alert("Error connecting to server"); }
});