from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

app = FastAPI(
    title="COCO",
    description="Your personal AI assistant",
    version="1.0.0"
)

# CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# HOME PAGE
@app.get("/", response_class=HTMLResponse)
async def home():
    with open("backend/static/index.html", "r", encoding="utf-8") as f:
        return f.read()

# CHAT PAGE
@app.get("/chat-ui", response_class=HTMLResponse)
async def chat_ui():
    with open("backend/static/chat.html", "r", encoding="utf-8") as f:
        return f.read()

# CHAT API
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")

    if not message:
        return JSONResponse({"reply": "Say something to COCO 🧠"})

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return JSONResponse({"reply": "GROQ API key missing"})

    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": "You are COCO, a hacker-style AI assistant."},
                    {"role": "user", "content": message}
                ]
            },
            timeout=30
        )

        reply = r.json()["choices"][0]["message"]["content"]
        return {"reply": reply}

    except Exception as e:
        return {"reply": f"Error: {str(e)}"}
