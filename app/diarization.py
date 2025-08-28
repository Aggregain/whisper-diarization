from pyannote.audio.pipelines import SpeakerDiarization
from app.config import Config

pipeline = SpeakerDiarization.from_pretrained("pyannote/speaker-diarization-3.1")
pipeline.to("cuda")

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
