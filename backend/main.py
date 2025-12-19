from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# ======================
# HOME PAGE (/)
# ======================
@app.get("/", response_class=HTMLResponse)
def home():
    with open("backend/static/index.html", "r", encoding="utf-8") as f:
        return f.read()

# ======================
# CHAT UI (/chat-ui)
# ======================
@app.get("/chat-ui", response_class=HTMLResponse)
def chat_ui():
    with open("backend/static/chat.html", "r", encoding="utf-8") as f:
        return f.read()

# ======================
# CHAT API
# ======================
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    return {
        "reply": f"Hello! You said: {req.message}",
        "mode_used": "chat"
    }
