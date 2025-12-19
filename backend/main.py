from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- STATIC FILES ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ---------- HOME PAGE ----------
@app.get("/")
def home():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

# ---------- CHAT PAGE ----------
@app.get("/chat-ui")
def chat_ui():
    return FileResponse(os.path.join(STATIC_DIR, "chat.html"))

# ---------- API ----------
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    return {
        "reply": f"Hello! You said: {req.message}",
        "mode_used": "chat"
    }
