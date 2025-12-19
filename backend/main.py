from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# HOME PAGE
@app.get("/", response_class=HTMLResponse)
async def home():
    with open("backend/static/index.html", "r") as f:
        return f.read()

# CHAT PAGE
@app.get("/chat-ui", response_class=HTMLResponse)
async def chat_ui():
    with open("backend/static/chat.html", "r") as f:
        return f.read()

# CHAT API
@app.post("/chat")
async def chat(data: dict):
    msg = data.get("message", "")
    return {
        "reply": f"Hello! I am COCO 🤖. You said: {msg}",
        "mode_used": "chat"
    }

# RESET CHAT
@app.post("/reset")
async def reset():
    return {"status": "cleared"}
