from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from groq import Groq

app = FastAPI()

# Serve frontend files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    message: str

# Home page
@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

# Chat UI
@app.get("/chat-ui", response_class=HTMLResponse)
def chat_ui():
    with open("static/chat.html", "r", encoding="utf-8") as f:
        return f.read()

# Chat API
@app.post("/chat")
def chat(req: ChatRequest):
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": req.message}]
    )
    return {"reply": completion.choices[0].message.content}
