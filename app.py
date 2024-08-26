from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from gtts import gTTS
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins. For production, specify allowed origins explicitly.
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods. For production, specify allowed methods explicitly.
    allow_headers=["*"],  # Allow all headers. For production, specify allowed headers explicitly.
)


class TextToSpeechRequest(BaseModel):
    text: str


@app.post("/speak")
async def speak(request: TextToSpeechRequest):
    text = request.text

    tts = gTTS(text, lang='pl')

    file_path = "output.mp3"
    tts.save(file_path)

    return FileResponse(file_path, media_type="audio/mpeg", filename="speech.mp3")
