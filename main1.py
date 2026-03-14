from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import random
from datetime import datetime
import io
import librosa
import numpy as np

app = FastAPI(title="🧠 MindCare API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str

def detect_emotions(text: str) -> List[str]:
    text_lower = text.lower()
    crisis_keywords = ["suicide", "kill myself", "end my life", "i want to die", "hopeless", "self-harm"]
    if any(keyword in text_lower for keyword in crisis_keywords):
        return ["crisis"]
    
    emotion_patterns = {
        "sadness": ["sad", "depressed", "down", "cry", "hurt", "alone"],
        "anger": ["angry", "mad", "furious", "hate", "frustrated"],
        "fear": ["anxious", "scared", "worry", "nervous", "panic"],
        "joy": ["happy", "great", "excited", "love", "amazing"],
        "neutral": ["ok", "fine", "normal", "checking"]
    }
    
    for emotion, keywords in emotion_patterns.items():
        if any(keyword in text_lower for keyword in keywords):
            return [emotion]
    return ["neutral"]

def generate_response(emotion: str, text: str) -> str:
    responses = {
        "crisis": "💔 **EMERGENCY** - You are NOT alone!\n\n🇮🇳 **CALL:** 1800-599-0019 (24×7)\n📱 **WhatsApp:** +91 9152987821\n\n**Someone cares. Please call NOW.**",
        "sadness": "🌸 I'm so sorry you're feeling sad. 💕 I'm right here with you. What's weighing on your heart?",
        "anger": "🔥 That sounds really frustrating. 🌿 Let's breathe: inhale 4, hold 4, exhale 6.",
        "fear": "🌺 Anxiety feels heavy. 💙 Try breathing: in 4 seconds, hold 4, out 6. You're safe here.",
        "joy": "🌈 That's beautiful! 🌟 Your happiness warms my heart! What made you smile?",
        "neutral": "☁️ Thank you for sharing. 🌼 How are you feeling beneath the surface?"
    }
    return responses.get(emotion, "💕 I'm listening with care. Tell me more.")

@app.post("/chat")
async def chat(message: Message):
    emotions = detect_emotions(message.text)
    primary_emotion = emotions[0] if emotions else "neutral"
    response = generate_response(primary_emotion, message.text)
    return {"emotion": primary_emotion, "emotions": emotions, "response": response}

@app.post("/voice")
async def voice_chat(file: UploadFile = File(...)):
    contents = await file.read()
    # Simple audio emotion (mock for demo - real librosa would need more setup)
    emotions = random.choice([["sadness"], ["joy"], ["neutral"], ["fear"]])
    return {
        "emotion": emotions[0],
        "response": f"🌸 I heard your voice! Detected {emotions[0]}. 💕 Thank you for sharing so openly.",
        "transcription": "I can hear your emotion clearly!"
    }

@app.get("/")
async def root():
    return {"status": "🧠 MindCare Backend Live"}
