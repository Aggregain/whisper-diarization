import torch
from app.config import Config
from pyannote.audio import Pipeline
import os

HF_TOKEN = os.getenv("HF_TOKEN")

try:
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=HF_TOKEN
    )
    pipeline.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
except Exception as e:
    raise RuntimeError(f"❌ Failed to load speaker diarization pipeline: {e}")


def diarize_audio(audio_path: str):
    diarization = pipeline(audio_path)
    results = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        results.append({
            "start": turn.start,
            "end": turn.end,
            "speaker": speaker
        })
    return results