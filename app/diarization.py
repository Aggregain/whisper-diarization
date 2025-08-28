import torch
from app.config import Config
from pyannote.audio import Pipeline

try:
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=Config.HF_TOKEN
    )
    pipeline.to(torch.device(Config.DEVICE if torch.cuda.is_available() else "cpu"))
except Exception as e:
    raise RuntimeError(f"❌ Failed to load speaker diarization pipeline: {e}")


def diarize_audio(audio_path: str):
    diarization = pipeline(audio_path)
    results = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        results.append({
            "start": round(turn.start, 2),
            "end": round(turn.end, 2),
            "speaker": speaker
        })
    return results
