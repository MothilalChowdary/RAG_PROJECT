const API_BASE = "http://127.0.0.1:8000";

// ----- Auth context handler -----
const loginLink = document.getElementById("loginLink");
const userStatus = document.getElementById("userStatus");

if (loginLink) {
    const token = sessionStorage.getItem("access_token");
    const username = sessionStorage.getItem("username");

    if (token) {
        if (userStatus) userStatus.innerText = `Signed in as: ${username || 'Authorized User'}`;
        loginLink.innerText = "Logout";
        loginLink.addEventListener("click", (e) => {
            e.preventDefault();
            sessionStorage.removeItem("access_token");
            sessionStorage.removeItem("username");
            window.location.reload();
        });
    } else {
        if (userStatus) userStatus.innerText = "Mode: Public Access (Limited sources)";
    }
}

// ----- Utility for loading states -----
function setLoading(btnId, loaderId, textId, isLoading) {
    const btn = document.getElementById(btnId);
    const loader = document.getElementById(loaderId);
    const text = document.getElementById(textId);

    if (btn) btn.disabled = isLoading;
    if (loader) loader.classList.toggle('hidden', !isLoading);
    if (text) text.classList.toggle('hidden', isLoading);
}

// ----- Login handler -----
document.getElementById("loginForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const errorDisplay = document.getElementById("loginError");

    errorDisplay.innerText = "";
    setLoading("loginBtn", "loginLoader", "loginText", true);

    try {
        const response = await fetch(`${API_BASE}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            sessionStorage.setItem("access_token", data.access_token);
            sessionStorage.setItem("username", username);
            window.location.href = "input.html";
        } else {
            errorDisplay.innerText = data.detail || "Login failed - invalid credentials";
        }
    } catch (error) {
        errorDisplay.innerText = "Connection error. Is the server running?";
    } finally {
        setLoading("loginBtn", "loginLoader", "loginText", false);
    }
});

// ----- Ask question handler -----
document.getElementById("askBtn")?.addEventListener("click", async () => {
    const queryInput = document.getElementById("query");
    const query = queryInput.value.trim();
    const token = sessionStorage.getItem("access_token");

    if (!query) return;

    setLoading("askBtn", "btnLoader", "btnText", true);
    const resultSection = document.getElementById("resultSection");
    const answerDiv = document.getElementById("answer");
    const sourcesList = document.getElementById("sources");

    const headers = { "Content-Type": "application/json" };
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_BASE}/`, {
            method: "POST",
            headers: headers,
            body: JSON.stringify({ query })
        });

        const data = await response.json();

        if (response.ok) {
            // data.response is [answer, sources]
            const [answer, sources] = data.response;

            // Clean display of answer (handling potential nulls)
            answerDiv.innerText = answer || "No specific answer found in context.";
            sourcesList.innerHTML = "";

            if (sources && sources.length > 0) {
                sources.forEach(src => {
                    const li = document.createElement("li");
                    li.innerText = src;
                    sourcesList.appendChild(li);
                });
            } else {
                sourcesList.innerHTML = "<li>No specific sources tagged</li>";
            }

            resultSection.classList.remove("hidden");
        } else {
            if (response.status === 401) {
                alert("Unauthorized. Redirecting to login.");
                window.location.href = "login.html";
            } else {
                answerDiv.innerText = "Error: " + (data.detail || "Unable to fetch answer.");
                resultSection.classList.remove("hidden");
            }
        }

    } catch (error) {
        console.error("Fetch error:", error);
        answerDiv.innerText = "Network error. Please ensure the backend is active.";
        resultSection.classList.remove("hidden");
    } finally {
        setLoading("askBtn", "btnLoader", "btnText", false);
    }
});