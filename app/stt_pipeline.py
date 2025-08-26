from faster_whisper import WhisperModel
from app.config import Config

whisper_model = WhisperModel(
    Config.WHISPER_MODEL, device=Config.DEVICE, compute_type=Config.COMPUTE_TYPE
)

def transcribe_audio(audio_path: str):
    segments, info = whisper_model.transcribe(audio_path, beam_size=5)
    results = []
    for seg in segments:
        results.append({
            "start": seg.start,
            "end": seg.end,
            "text": seg.text.strip()
        })
    return results
