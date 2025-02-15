from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
# from gtts import gTTS
from fastapi.middleware.cors import CORSMiddleware
import os
import warnings
import torch

from InferenceInterfaces.ToucanTTSInterface import ToucanTTSInterface
from Utility.storage_config import MODELS_DIR

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins. For production, specify allowed origins explicitly.
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods. For production, specify allowed methods explicitly.
    allow_headers=["*"],  # Allow all headers. For production, specify allowed headers explicitly.
)

warnings.filterwarnings("ignore", category=UserWarning)

PATH_TO_TTS_MODEL = os.path.join(MODELS_DIR, "ToucanTTS_Polish", "checkpoint_42.pt")
PATH_TO_VOCODER_MODEL = None  # os.path.join(MODELS_DIR, "BigVGAN", "best.pt")
PATH_TO_REFERENCE_SPEAKER = ""  # audios/speaker_references_for_testing/female_high_voice.wav
LANGUAGE = "pl"
device = "cuda" if torch.cuda.is_available() else "cpu"

tts = ToucanTTSInterface(device=device, tts_model_path=PATH_TO_TTS_MODEL, vocoder_model_path=PATH_TO_VOCODER_MODEL, faster_vocoder=device == "cuda")
tts.set_language(lang_id=LANGUAGE)
if PATH_TO_REFERENCE_SPEAKER != "":
    if os.path.exists(PATH_TO_REFERENCE_SPEAKER):
        tts.set_utterance_embedding(PATH_TO_REFERENCE_SPEAKER)
    else:
        print(f"File {PATH_TO_REFERENCE_SPEAKER} could not be found, please check for typos and re-run. Using default for now.")

print("Loading the following configuration:")
print(f"\tTTS Model: {PATH_TO_TTS_MODEL}")
print(f"\tVocoder Model: {PATH_TO_VOCODER_MODEL}")
print(f"\tReference Audio: {PATH_TO_REFERENCE_SPEAKER}")
print(f"\tLanguage Used: {LANGUAGE}")
print(f"\tDevice Used: {device}")


class TextToSpeechRequest(BaseModel):
    text: str


@app.post("/speak")
async def speak(request: TextToSpeechRequest):
    text = request.text

    # tts = gTTS(text, lang='pl')
    file_path = "output.wav"
    tts.read_to_file(
        [text],
        file_path,
        duration_scaling_factor=1.0,
        pitch_variance_scale=1.0,
        energy_variance_scale=1.0,
        silent=False,
        dur_list=None,
        pitch_list=None,
        energy_list=None,
        increased_compatibility_mode=False
    )
    # tts.save(file_path)
    return FileResponse(file_path, media_type="audio/wav", filename="speech.wav")
