from fastapi import FastAPI
from pydantic import BaseModel
import os
from groq import Groq
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Serve frontend
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
            {"role": "system", "content": "You are COCO, a cool hacker-style AI assistant for youth."},
            {"role": "user", "content": req.message}
        ],
        temperature=0.7
    )

    return {
        "reply": response.choices[0].message.content
    }
