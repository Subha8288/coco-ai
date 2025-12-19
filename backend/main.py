from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI()

# Groq client (REAL AI)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Serve static files
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

@app.get("/")
def home():
    return FileResponse("backend/static/index.html")

@app.get("/chat-ui")
def chat_ui():
    return FileResponse("backend/static/chat.html")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are COCO_AI, a futuristic hacker-style AI. "
                    "You answer intelligently, creatively, and confidently. "
                    "You NEVER repeat the user's input. "
                    "You speak like a next-generation AI for youth."
                )
            },
            {
                "role": "user",
                "content": req.message
            }
        ],
        temperature=0.85,
        max_tokens=300
    )

    return {
        "reply": response.choices[0].message.content.strip()
    }
