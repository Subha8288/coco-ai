from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

# ================= APP =================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= CONFIG =================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# ✅ WORKING GROQ MODEL
MODEL = "llama-3.1-8b-instant"

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY environment variable is not set")

# ================= MEMORY =================
CHAT_MEMORY = []
MAX_MEMORY = 5

# ================= REQUEST =================
class ChatRequest(BaseModel):
    message: str
    mode: str | None = None

# ================= COCO IDENTITY =================
BASE_IDENTITY = (
    "You are COCO, a custom AI assistant built for students. "
    "Your name is COCO. "
    "Never say you are OpenAI, ChatGPT, or a large language model. "
    "If asked your name, always reply exactly: 'I am COCO.' "
    "Be friendly, clear, and helpful."
)

PROMPTS = {
    "study": BASE_IDENTITY + " Explain concepts step by step in simple words.",
    "coding": BASE_IDENTITY + " Help with coding clearly and patiently.",
    "writing": BASE_IDENTITY + " Help with writing emails and documents.",
    "chat": BASE_IDENTITY + " Chat naturally like a friendly assistant.",
    "care": BASE_IDENTITY + " Be calm, kind, and supportive. Never encourage self-harm."
}

# ================= INTENT =================
def detect_intent(text: str):
    t = text.lower()
    if any(w in t for w in ["sad", "depressed", "lonely", "anxious"]):
        return "care"
    if any(w in t for w in ["code", "error", "bug", "python", "java"]):
        return "coding"
    if any(w in t for w in ["write", "email", "letter", "essay"]):
        return "writing"
    if any(w in t for w in ["explain", "what is", "define"]):
        return "study"
    return "chat"

# ================= CHAT =================
@app.post("/chat")
def chat(req: ChatRequest):
    mode = req.mode if req.mode else detect_intent(req.message)
    system_prompt = PROMPTS.get(mode, PROMPTS["chat"])

    history = ""
    for m in CHAT_MEMORY:
        history += f"User: {m['user']}\nCOCO: {m['ai']}\n"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": history + "\nUser: " + req.message}
    ]

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.4
    }

    try:
        r = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        data = r.json()

        if "choices" not in data:
            return {
                "reply": "COCO is temporarily unavailable. Please try again.",
                "details": data
            }

        reply = data["choices"][0]["message"]["content"].strip()

        CHAT_MEMORY.append({"user": req.message, "ai": reply})
        if len(CHAT_MEMORY) > MAX_MEMORY:
            CHAT_MEMORY.pop(0)

        return {
            "reply": reply,
            "mode_used": mode
        }

    except Exception as e:
        return {
            "reply": "COCO encountered an error.",
            "error": str(e)
        }

# ================= RESET =================
@app.post("/reset")
def reset():
    CHAT_MEMORY.clear()
    return {"status": "memory cleared"}
