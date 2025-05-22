from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import requests
import os

app = FastAPI()

# Allow frontend access (e.g., GitHub Pages or local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with specific frontend URL if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route serving a simple frontend HTML page
@app.get("/", response_class=HTMLResponse)
def home():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Code Maker Frontend</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { color: #4CAF50; }
            textarea { width: 100%; height: 150px; }
            button { padding: 10px 20px; margin-top: 10px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
            button:hover { background-color: #45a049; }
            pre { background-color: #f4f4f4; padding: 10px; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <h1>Welcome to Code Maker Frontend!</h1>
        <textarea id="prompt" placeholder="Enter your prompt here..."></textarea><br/>
        <button onclick="generateCode()">Generate Code</button>
        <h3>Result:</h3>
        <pre id="result"></pre>

        <script>
            async function generateCode() {
                const prompt = document.getElementById('prompt').value;
                if (!prompt) {
                    alert("Please enter a prompt.");
                    return;
                }
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt })
                });
                const data = await response.json();
                if (data.result) {
                    document.getElementById('result').textContent = data.result;
                } else if (data.error) {
                    document.getElementById('result').textContent = "Error: " + data.error;
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content

# OpenRouter chat completion API
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.post("/generate")
async def generate_code(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",  # You can change this to another model on OpenRouter
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        completion = response.json()["choices"][0]["message"]["content"]
        return {"result": completion}
    else:
        return {"error": response.text}
